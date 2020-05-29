#coding:utf8
"""
The script is used to extract word tokens:
1. chinese word level ngram
2. character level ngram

There is a assumption that a single chinese word is treat as character
"""
from __future__ import absolute_import
import re
from functools import partialmethod, partial
from nltk import RegexpParser

from ._base import FileHanler
from ..base.exceptions import ArgumentInvalid

BOS = "<BOS/>"
EOS = "</EOS>"
UNK = "<UNK>"
DATE = "#DATE"
TIME = "#TIME"
NUMBER = "#NUM"
LINK = "#URL"
IMAG = "#IMG"
USER = "#USER"
FEE = "#FEE"
PHONE = "#PHONE"

# reference: https://www.qqxiuzi.cn/zh/hanzi-unicode-bianma.php
UNICODE_CHINESE_CHARSET = "[\u4E00-\u9FEF]" 

SPECIAL_TOKEN = [BOS, EOS, UNK, DATE, TIME, NUMBER, LINK, IMAG, USER, FEE, PHONE]

class SentenceProcess:
    def __init__(self, *, file=None, sentences=None):
        # Extract Text
        if file is not None:
            self.handler = FileHanler(file)
        else:
            self.handler = None

        # store sentences, if it's tuple, list or None, otherwise raise a exception
        if sentences is None:
            self.sentences = None
        elif isinstance(sentences, (tuple, list)):
            self.sentences = list(sentences)
        else:
            raise ValueError("Deal with multi lines, sentences must be tuple"
                        f"list. But get {type(sentences)}")


    @classmethod
    def _link_pattern(cls):
        """Link Pattern"""
        pattern = re.compile(
            r"""
            \<a\b [^\>\<]*\> # html tag a
            """, re.M|re.I|re.X
        )

        return pattern


    @classmethod
    def _link_no_tag_pattern(cls):
        """URL Link Without Tag"""
        pattern = re.compile(
            r"""
            (?<=[^a-z\:\"\'])https?://[^\s<>\"]+[a-zA-Z]|www\.[^\s<>\"]+[a-zA-Z0-9](?<![\<\>/])    # url link without tag
            """, re.M|re.I|re.X
        )

        return pattern



    @classmethod
    def _img_pattern(cls, alt_text=True):
        """Image Pattern

        Extract image pattern. If alt_text is True, get a additional pattern
        `alt_pattern` that can extract alternative text pattern
        """
        pattern = re.compile(r"\<img\b [^\>\<]*\>", re.M|re.I)

        if alt_text:
            # if alternative text being needed, extract the text, otherwise add IMAG
            alt_pattern = re.compile(r"alt=(?:\'|\")\[?(?P<txt>[\u4E00-\u9FEF]+)")
            return pattern, alt_pattern

        return pattern

    
    @classmethod
    def _date_pattern(cls, lang="cn", match="whole"):
        """Add Timestamp Token
        
        There are main two types of language: chinese(use `cn`), and 
        english(use `en`). Chinese language timestamp looks like:
        1. <num>年<num>月<num>日, it's `whole` match option
        2. <num>年, <num>年<num>月 and <num>月<num>日, those are `part` match
            option

        
        Args:
            text: string, it's string text
            lang: string, it's language type, `cn` is short of chinese, `en` is
                short of english
            match: string, choose a match type, if it's `whole`, must be whole
                match, `part` use partial match
        """
        if lang.lower() not in ["cn", "en"]:
            raise ArgumentInvalid(f"Can't support the language {lang}")
            
        if match.lower() not in ["whole", "part"]:
            raise ArgumentInvalid(f"Can't support the match mode {match}.")
    
        if match.lower() == "whole":
            pattern = re.compile(
                r"""
                (
                    (?:\d{2}年|\d{4}年|公元前?\d+年?)     # it's year format
                    (?:1[0-2]月|[^\d][1-9]月)   # month format
                    (?:[1-2][0-9]日|[^\d][1-9]日|[^\d]3[0-1]日)     # day format
                )
                """, re.VERBOSE)
        elif match.lower() == "part":
            pattern = re.compile(
                r"""
                (?<=[^\)\〕\]\}])
                (
                    (?:\d{4}[\-\/\\])?(?:1[0-2]|0?[1-9])[\-\/\\](?:[1-2][0-9]|0?[1-9]|3[0-1])| # english datetime <year>-<month>-<day>, <year>\<month>\<day>, <year>/<month>/<day>
                    # (?:1[0-2]|0?[1-9])月(?:[1-2][0-9]|0?[1-9]{1}|3[0-1]{1})日| # month day
                    (?:\d{2}年|\d{4}年|公元前?\d+年)?(?:1[0-2]|0?[1-9])月(?:[1-2][0-9]|0?[1-9]{1}日|3[0-1]{1})日| # year(optional) month and day
                    (?:\d{2}年|\d{4}年|公元前?\d+年?)份?| # year
                    (?:1[0-2]月|[1-9]{1}月)| # month
                    (?:[1-2][0-9]|[1-9]{1}|3[0-1]{1})(?:日|号)(?:凌晨|傍晚|中午|上午)?|
                    (?:\d{2}世纪(?:中叶|初|末|晚期)?)| # century
                    (?:(?:大概)?\d{1,3}多?[天月年]前?) # special time, eg:<大概>13<多>天<前>
                )
                """, re.VERBOSE)

        return pattern


    @classmethod
    def _time_pattern(cls):
        """Add Timestamp Token
        
        There are main two types of language: chinese(use `cn`), and 
        english(use `en`). There is an additional time mode <num>点<num>分, in 
        Chinese language time.
        """
        pattern = re.compile(
            r"""
            # (?<!\@)
            (
                (?:早上|晚上|下午|上午|凌晨)?(?:1[0-9]|2[0-3]|0?[0-9])[点时](?:左右)?(?=[^\d点时左右\:\：])|
                (?:早上|晚上|下午|上午|凌晨)?(?:1[0-9]|2[0-3]|[0-9])[\:\：点]?(?:[0-5]?[0-9](?:分钟?)?)(?:许|晚)?[\~\-](?:1[0-9]|2[0-3]|[0-9])[\:\：点]?(?:[0-5]?[0-9](?:秒?)?)(?:许|晚)?(?=[^\d点分时晚\:\：])|  # eg：上午6点～7点
                (?:早上|晚上|下午|上午|凌晨)?(?:1[0-9]|2[0-3]|0?[0-9])[点时\:\：](?:[0-5]?[0-9][分\:\：]?)(?:许|晚)?(?:[0-5]?[0-9]秒?)(?=[^\d分许晚\:\：])|    # chinese time
                (?:早上|晚上|下午|上午|凌晨)?(?:1[0-9]|2[0-3]|0?[0-9])[点时\:\：](?:[0-5]?[0-9][分\:\：]?)(?:许|晚)(?=[^\d分许晚\:\：])|    # chinese time
                # (?:早上|晚上|下午|上午|凌晨)?(?:0?0时|1[0-9]时|2[0-3]时|0?[0-9]时)(?:[0-5]?[0-9]分?)?(?:许|晚)?(?=[^\d分许晚])|
                # (?:早上|晚上|下午|上午|凌晨)?(?:0?0\:|1[0-9]\:|2[0-3]\:|0?[0-9]\:)(?:[0-5]?[0-9]\:)(?:[0-5]?[0-9])(?=[^\d\:])|  # english time
                # (?:早上|晚上|下午|上午|凌晨)?(?:0?0\:|1[0-9]\:|2[0-3]\:|0?[0-9]\:)(?:[0-5]?[0-9])分?(?=[^\d分\:])|         # english time without seconds
                (?:(?:大概|都?不到)?\d{1,2}多?[分秒时][钟前]?(?:左右)?)(?=[^\d分秒许晚时点])
            )
            """, re.VERBOSE)

        return pattern


    @classmethod
    def _user_pattern(cls, exclude_email=True):
        """Extract User Name

        Extract user name with first char is `@`. Maybe, the email domain name can
        be extracted. If exclude_email is True, add a email pattern.

        Args:
            text: string, string text
            exclude_email: boolean, if True, return a email host name pattern. 
                Otherwise return raw user pattern
        
        Results:
            pattern: regex pattern being compiled, it's raw user pattern
            email_pattern: regex pattern being compiled, it's email host pattern
        """
        pattern = re.compile(
            r"""
            (
                (?:\()?@[\_a-z0-9\.\_\-\u4E00-\u9FEF]+(?:\：|\))?|   # @<username>
                (?:[\(\（]?id[\:\：\ ]?[\_a-z0-9]+[\)\）]?|[\(\（]id[\:\ \：]?[\_a-z0-9]+[\)\）]?)|    # [id: <username>
                (?:[\(（]?微信号?：?[\_a-z0-9]+\)?|[\(（]?微信号?: ?[\_a-z0-9]+[\)）]?)|     # 微信号: <username>
                (?:[\(（]?微信公众号：?[\_a-z0-9]+\)?|[\(（]?微信公众号: ?[\_a-z0-9]+[\)）]?)|     # 微信号: <username>
                (?:[\(（]?v信号?：?[\_a-z0-9]+\)?|[\(（]?v信号?: ?[\_a-zA-Z0-9]+[\)）]?)|
                (?:[\(（]?Wechat\ *[\:\：]?\ *[\_a-z0-9]+\)?|[\(（]?Wechat\ *[\:\：]?\ *[\_a-z0-9]+[\)）]?)
            )
            """, re.X|re.I
        )

        # email maybe matched, if exclude_email True, remove the email
        if exclude_email:
            email_pattern = re.compile(r"@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){1,3}")
            return pattern, email_pattern
        
        return pattern


    @classmethod
    def _fee_pattern(cls):
        """Extract Fee Pattern"""
        pattern = re.compile(
            r"""
            (
                (?<=[\u4E00-\u9FEF])\d+[万千亿百\d]*\.?\d*余?[万千亿百]?元|
                (?<=[(?:工资)|(?:试用期)|(?:试用期后)|(?:收入)|(?:待遇)|(?:补贴)|(?:底薪)])[\:\ \：=]?(?:(?:[\d\.]+)元?[\~\-\～])?(?:\d+元)(?:\/[月日年周小时]|每[月日年周小时])?|
                [\d多万千亿\,]+ \.?[\d\,]+(?:元|欧元|美元|\$)(?:左右)?
                # (?:费用)?(?:人民币|美元|欧元)(?:共计|等)? # head
                # [\d\.多万千亿余]+(?:元|欧元|美元|\$)(?:左右)?

                # (?<=[^a-z\u4E00-\u9FEF])[\:\ ]?[\d\.]+(?:元|欧元|美元|\$)[\/每][周日年月]
            )
            """, re.VERBOSE
        )

        return pattern


    @classmethod
    def _phone_pattern(cls):
        """Phone Number Pattern"""
        pattern = re.compile(
            r"""
            (
                (?:(?:(?:客服|联系|客服咨询|客户咨询|热线)?电话|热线|传真|手机|拨打|电话号码|平台商务合作|商务合作|合作)
                [\:：\/]?\ *(?:0\d{,3}[\_\ \-]{1,2}\d{7,13}\ *(?:电话)?|   # landline phone number
                (?:\+86)?\ *1[3-9][0-9]{9}| # mobile phone number
                (?:\+86)?\ *1[3-9]\-[0-9]{4}\-[0-9]{4}| # mobile phone number
                (?:400[ \-]?\d{3,4}[\- ]?\d{4,5}))(?:转\d+)?)| # 400 phone
                (?:12\d{3,5}电话)| # phone number stars with 12
                (?:(?:举报)?电话[\:\：\ ](?:110|120|114|119))|
                (?:热线)?电话[\:\：\ \(\（]?(?:\d{7,13}|0\d{2,3}[\_\-\ \～\~]{,2}\d{7,13})[\ \)\）]?
            )
            """, re.VERBOSE
        )
        return pattern


    @classmethod
    def _number_pattern(cls):
        """Number Pattern"""
        pattern = re.compile(
            r"""
            # 
            (
                (?:
                    (?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])[第每约]?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾兆百佰千仟亿万]+[点\.]?[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖]{0,}(?:多|余|余万|\/)?[次岁件座方枚箱级米斤个户楼天名部人项\%\％瓶号粒位亩页盒吨室条℃艘块辆张本案起例条套双度份°C㎡百万亿]{1,2}次?[儿]?|
                    (?<=[^a-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])第?[1-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]+号?房间?|   # room number
                    (?<=[^a-ln-oq-z1-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])(?:pm)[\d一二三四五六七八九十点\.]{2,6}|    # PM value
                    (?<=[^a-z])[gcdztspkxly]\d{1,4}(?<![^\da-z\u4E00-\u9FEF])|    # railway number
                    (?<=[^a-eg-ln-z0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])FM[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点\.]{2,6}(?:mhz|hz|ghz)?| # raidio frequency
                    (?<=[^a-z0-9十百千万亿一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点\.]{1,}[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]+(?:mg|kg|cm|dm|mb|gb|ml|hz|mhz|ghz|m|b|w|l|g)(?<![^a-z0-9十百千万亿一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])|
                    (?<=[^0-9十百千万亿兆一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾])(?:合计|小计|共|超过)?[十百千万亿\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾点兆\.]{1,}[\d一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]+多?(?:毫克|千克|人次|毫升|公斤|千亩|公里|千米|厘米|分米|平方米|平米|平方分米|平方厘米|平方千米|比特|字节|千瓦|毫瓦|张本|周岁|荷兹|克|升|斤|里|米|瓦|岁)倍?(?:左右)?
                )|
                (?:(?:第|仅仅|仅仅第)?[0-9一二三四五六七八九十壹贰叁肆伍陆柒捌玖拾]{1,3}天后?)|
                (?:[0-9]{1,3}行车道?)|
                (?:国道\d{1,4}线?)|
                (?:\d{1,4}国道线?)|
                (?:(?:次数)[\:\：]\d{1,})   #次数：12
            )
            """, re.I | re.X
        )

        return pattern



    def remove(self, text, pattern):
        """Remove String Matched

        If pattern match strings in text, remove the strings. If pattern is 
        re.Pattern, use pattern method sub with repl string ""; if it's string,
        use the string method replace

        Args:
            text: string text
            pattern: string or re.Pattern

        Results:
            result: text is removed string matched pattern
        """
        if isinstance(pattern, str):
            text = text.replace(pattern, "")
        elif isinstance(pattern, re.Pattern):
            text = pattern.sub("", text)
        else:
            raise Exception(f"Can't deal with pattern: {pattern}")

        return text


    @property
    def available_pattern(self):
        patterns = [i for i in self.__dir__() if i.endswith("pattern")]
        return patterns



    def update(self, pattern_func, text, *, token=None, method="remove", **kwargs):
        """Update String With Pattern

        Use pattern function to generate patterns. If use `remove` method, remove
        string matched with pattern and replace the string with token, or 
        `extract` method, add the token and don't remove string.

        Args:
            pattern_func: callable function, it's the pattern function
            text: string, string text
            token: string, special token, append the token followed by the text
                default use the token like #URL, #IMG, and so on
            method: string, choose how to deal with string matched, if `remove`,
                remove the string matched, if `extract`, keep the string matched
            kwargs: key-word parameters that are treat as pattern_func parameters

        
        Examples:
            >>> text = "问众智能携手新双立集团、四川终端公司打造中国首个车联网销售...,2017年10月11日，成都】问众智能携手12:30"
            >>> process = feature_extraction.SentenceProcess()
            >>> process.update(process._date_pattern, text, token="#DATE", method="extract")
                '问众智能携手新双立集团、四川终端公司打造中国首个车联网销售...,2017年10月11日 #DATE ，成都】问众智能携手12:30'
            >>> process.update(process._date_pattern, text, token="#DATE", method="remove")
                '问众智能携手新双立集团、四川终端公司打造中国首个车联网销售..., #DATE ，成都】问众智能携手12:30
        """
        if not hasattr(self, pattern_func.__name__):
            raise Exception("Object supports regular pattern: %s" % (", ".join(self.available_pattern)))
        

        patterns = pattern_func(**kwargs)
        # if pattern_func is image pattern, and get the alt_pattern, extract 
        # alternative text
        if pattern_func.__name__ == "_img_pattern":
            if isinstance(patterns, tuple):
                replace_func = partial(self.replace_with_2nd_pattern, \
                    pattern= patterns[1], token=token)
                text = patterns[0].sub(replace_func, text)
            else:
                replace_func = partial(self.replace_with_2nd_pattern, \
                    pattern=None, token=token)
                text = patterns[0].sub(replace_func, text)
        elif pattern_func.__name__ == "_user_pattern":
            if isinstance(patterns, tuple):
                replace_func = partial(self.replace_with_2nd_pattern, \
                    pattern= patterns[1], token=token, method="remove")
                text = patterns[0].sub(replace_func, text)
            else:
                replace_func = partial(self.available_pattern, \
                    pattern=None, token=token, method="remove")
                text = patterns[0].sub(replace_func, text)
        else:
            replace_func = partial(self.replace_with_2nd_pattern, \
                token=token, method=method)
            text = patterns.sub(replace_func, text)

        return text



    def replace_with_2nd_pattern(self, matchobj, pattern=None, token=None, \
        method="extract"):
        """Sub Callable Function

        It's a callable function to be used in the `re.sub()` or `pattern.sub()`
        method. That can deal with matched string. If it's `img` tag, add token
        after text
        """
        text = matchobj.group(0)

        # # firstly add token
        # text = text + f" {token} "
        if token is None:
            token = ""

        if method == "extract":
            if pattern is not None and pattern.findall(text):
                result = text +  " ".join(pattern.findall(text)) + f" {token} "
            else:
                result = text + f" {token} "
        elif method == "remove":
            if pattern is not None and pattern.findall(text):
                result = " ".join(pattern.findall(text)) + f" {token} "
            else:
                result = f" {token} "
        return result


    def process_pipeline(self, text, link_option="extract"):
        text = self.update(self._link_pattern, text, token=LINK, method=link_option)
        text = self.update(self._img_pattern, text, token=IMAG, method="extract")
        text = self.update(self._link_no_tag_pattern, text, token=LINK, method="remove")
        # remove the space
        pattern = re.compile(r"(?<=[^a-z\"\'\-\_\<\>])\s+(?=[^a-z\"\'\-\_\<\>])", re.I)
        # pattern = re.compile(r"(?<=[\d\u4E00-\u9FEF])\s+", "", text) #text.replace(" ", "")
        text = pattern.sub("", text)
        text = self.update(self._date_pattern, text, token=DATE, method="remove", match="part")
        text = self.update(self._time_pattern, text, token=TIME, method="remove")
        text = self.update(self._user_pattern, text, token=USER, method="remove")
        text = self.update(self._fee_pattern, text, token=FEE, method="remove")
        text = self.update(self._phone_pattern, text, token=PHONE, method="remove")
        text = self.update(self._number_pattern, text, token=NUMBER, method="remove")

        # some string are non-sense, remove those string
        pattern = re.compile(
            r"""
            原文链接|
            转发微博|
            看.支持请转！|
            \u200b|
            \xa0[2-7·]?|
            \u2003|
            ↓|
            ↑|
            ★|
            ❤|
            ▶|
            ▲|
            ▼|
            整理发布|
            转载请注明|
            长按识别二维码关注我们|
            查看更多|
            特别声明：以上文章内容仅代表作者本人观点，.+看点联系。?|
            声明：本文内容及图片均来源网络，全部转载，内容未经核实，如有问题，请联系我们删除。?|
            版权声明：如涉及版权问题，请.+联系。？|
            请点.{1,15}关注.{1,10}号(?:，谢谢)?|
            如有侵权.{1,15}进行删除(?:，谢谢)?|
            点击.{1,10}原文，看更多.{1,4}消息|
            请点击本行文字.+联系原出处。？
            """, re.X)
        text = pattern.sub("", text)
        return text