from agent.tools.send_message import send_message, send_message_multiple





if __name__ == '__main__':
    message = '''Alo 1234'''
    profile_url = 'https://www.linkedin.com/in/selenado/'
    msg_url = {
        'https://www.linkedin.com/in/thinh-nguyen-aa3887165/': message,
        'https://www.linkedin.com/in/selenado/': message,
        'https://www.linkedin.com/in/soilangcon/': message
    }

    send_message(message,profile_url)
    # send_message_multiple(msg_url=msg_url)