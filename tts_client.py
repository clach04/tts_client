#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import sys

try:
    from urllib.parse import urlencode
except ImportError:
    # Probably Python2
    from urllib import urlencode
    


class BaseClientTTS(object):
    """Base TTS CLient"""
    def gen_url(self, text, lang='en', voice=None, mime_type='audio/mp3'):
        raise NotImplementedError()

class GoogleTranslate(BaseClientTTS):
    """Use google translate TTS interface"""
    def gen_url(self, text, lang='en', voice=None, mime_type='audio/mp3'):
        # voice ignored
        if mime_type != 'audio/mp3':
            raise NotImplementedError("mime_type != 'audio/mp3'")  # FIXME need a new/different exception
        base_url = os.environ.get('GOOGLE_TRANSLATE_URL', 'https://translate.google.com/translate_tts?')
        vars = {
            'q': text,
            'l': lang,
            'tl': lang,
            'client': 'tw-ob',
            'ttsspeed': 1,
            'total': 1,
            'ie': 'UTF-8',
            # looks like can get away with out 'textlen'
        }
        result = base_url + urlencode(vars)
        mime_type = 'audio/mp3'
        return result, mime_type


class OpenTTS(BaseClientTTS):
    """Use Open Text to Speech Server interface from https://github.com/synesthesiam/opentts"""
    def _gen_url(self, text, lang='en', voice=None, mime_type='audio/wav'):
        # voice ignored
        base_url = os.environ.get('OPEN_TTS_URL', 'http://localhost/api/tts?')
        voice = 'espeak:%s' % lang  # TODO ignores parameter
        vars = {
            'text': text,
            'voice': voice,
        }
        result = base_url + urlencode(vars)
        return result, mime_type

    def gen_url(self, text, lang='en', voice=None, mime_type='audio/wav'):
        if mime_type != 'audio/wav':
            raise NotImplementedError("mime_type != 'audio/wav'")  # FIXME need a new/different exception

        result = self._gen_url(text, lang=lang, voice=voice, mime_type=mime_type)
        return result

class OpenTTSMp3(OpenTTS):
    """Non-standard OpenTTS server that only serves mp3 format, e.g. https://github.com/clach04/srttss"""
    def gen_url(self, text, lang='en', voice=None, mime_type='audio/mp3'):
        if mime_type != 'audio/mp3':
            raise NotImplementedError("mime_type != 'audio/mp3'")  # FIXME need a new/different exception

        result = self._gen_url(text, lang=lang, voice=voice, mime_type=mime_type)
        return result



def main(argv=None):
    if argv is None:
        argv = sys.argv

    print(sys.platform, sys.version)
    text = 'hello world'
    for engine in [GoogleTranslate(), OpenTTS(), OpenTTSMp3()]:
        url = engine.gen_url(text)
        print(url)

    return 0


if __name__ == "__main__":
    sys.exit(main())

