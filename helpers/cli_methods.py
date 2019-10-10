import requests, logging, shlex
from subprocess import Popen, PIPE

def send_command_to_cli_and_receive_text(cli_command):
    args = shlex.split(''.join((cli_command)))
    p = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    text = p.communicate()

    # convert to list because tuple is immutable
    textlist = list(text)

    # strip error code element
    if textlist[0] == b'': del textlist[0]
    else: del textlist[1]

    # remove final line feed
    textlist[-1] = textlist[-1].strip()

    # convert any returned Unicode bytes to string
    for item in range(len(textlist)):
        # filter out any bytes unconvertable to string
        if type(textlist[item]) is bytes: textlist[item] = textlist[item].decode('UTF-8', 'surrogateescape')

    # convert back to tupl
    text = tuple(textlist)

    p.stdin.close()
    return ''.join(text)