import datetime
import os
import re

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]
client = openai.OpenAI()

# ========

def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument('--input', default=None, required=True)
    #parser.add_argument('--output', default='askailog.md')

    parser.add_argument('--use-ssl', default=None)

    args = parser.parse_args()
    return args

# ========

def ask(prompt):
    response = client.chat.completions.create(
      #model='o3-mini',
      #model='gpt-5',
      #model='gpt-4o',,
      model='gpt-5.2',
      #model='gpt-4.1',
      #model='gpt-4o-mini',
      #model='gpt-4.1-mini',
      messages=[
            {'role': 'user', 'content': prompt},
      ],
      timeout=130
    )
    return response

def todaystr_long():
    todaydt = datetime.datetime.today()
    datestr = todaydt.strftime('%Y/%m/%d')
    timestr = todaydt.strftime('%H:%M:%S')

    wd =  todaydt.weekday()
    dow_j = ['月','火', '水', '木','金','土','日'][wd]
    dow_e = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][wd]

    return f'{datestr} {dow_e} {timestr}'

def file2str(filepath):
    ret = ''
    with open(filepath, encoding='utf8', mode='r') as f:
        ret = f.read()
    return ret

def str2file(filepath, s):
    with open(filepath, encoding='utf8', mode='w') as f:
        f.write(s)

LB = '\n'
def string2lines(s):
    return s.split(LB)
def lines2string(lines):
    return LB.join(lines)

class Outputter:
    def __init__(self, prompt, response):
        self._response = response

        self._todaystr = todaystr_long()

        self._prompt = prompt
        self._answer = response.choices[0].message.content
        self._answer_role = response.choices[0].message.role
        self._consumed_prompt_token = response.usage.prompt_tokens
        self._consumed_completion_token = response.usage.completion_tokens

    def out(self):
        raise NotImplementedError

class Logger(Outputter):
    def __init__(self, prompt, response):
        super().__init__(prompt, response)
        self._logfilepath = 'PLEASE_GIVE_EXPLICITLY__askailog.md'

    def set_target_filepath(self, markdown_filepath):
        self._logfilepath = markdown_filepath

    def out(self):
        prependee = f"""# {self._todaystr} {self._consumed_prompt_token} {self._consumed_completion_token}
{self._prompt}
{self._answer}"""

        logcontent = file2str(self._logfilepath)

        outstr = f"""{prependee}

{logcontent}"""

        str2file(self._logfilepath, outstr)

class Stdouter(Outputter):
    def __init__(self, prompt, response):
        super().__init__(prompt, response)

    def out(self):
        print('=== prompt ===')
        print(self._prompt)
        print('')

        print('=== answer ===')
        print(self._answer)
        print('')

        print(f'tokens : prompt {self._consumed_prompt_token}, completion {self._consumed_completion_token}')

class SimpleStdouter(Outputter):
    def __init__(self, prompt, response):
        super().__init__(prompt, response)

    def out(self):
        summary = self._prompt[:16]
        print(f'{summary}({self._consumed_prompt_token}->{self._consumed_completion_token})..., Done.')

class Appender(Outputter):
    def __init__(self, prompt, response):
        super().__init__(prompt, response)
        self._filepath = 'PLEASE_GIVE_EXPLICITLY_APPENDER_NAME.md'
        NEW_BLANKLINE = '\n'
        self._content = f'{self._prompt}{NEW_BLANKLINE}{self._answer}{NEW_BLANKLINE}'

    def set_target_filepath(self, markdown_filepath):
        self._filepath = markdown_filepath

    def out(self):
        str2file(self._filepath, self._content)

def convert_scrapbox_tab_to_space(text):
    newtext = re.sub(r'^\t', ' ', text, flags=re.MULTILINE)
    return newtext

# ========

args = parse_arguments()
if args.use_ssl:
    os.environ['REQUESTS_CA_BUNDLE'] = args.use_ssl
promptfilename = args.input
if not os.path.exists(promptfilename):
    raise RuntimeError(f'Please prepare the prompt file {promptfilename}.')

q = file2str(promptfilename)
prompt=q

response = ask(prompt)

#logger = Logger(prompt, response)
#logger.set_target_filepath(args.output)
appender = Appender(prompt, response)
appender.set_target_filepath(promptfilename)

#logger.out()
appender.out()
