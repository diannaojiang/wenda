import llms.gpt4free.forefront as openai_api

def chat_init(history):
    # history_data  = [
    #     {
    #         'is_sent': True,
    #         'message': 'my name is Tekky'
    #     },
    #     {
    #         'is_sent': False,
    #         'message': 'hello Tekky'
    #     }
    # ]
    history_data = []
    if history is not None:
        history_data = []
        for i, old_chat in enumerate(history):
            if  old_chat['role'] == "user":
                history_data.append({
                    'is_sent': True,
                    'message': old_chat['content']
                })
            elif old_chat['role'] == "AI" or old_chat['role'] == 'assistant':
                history_data.append({
                    'is_sent': False,
                    'message': old_chat['content']
                })
    return history_data


def chat_one(prompt, history_formatted, max_length, top_p, temperature, zhishiku=False):
    for response in openai_api.StreamingCompletion.create(
        account_data=token, 
        prompt=prompt, 
        model='gpt-4'
        ):
        yield response.choices[0].text


token = None


def load_model():
    global token
    print("create account (3-4s)")
    # create an account
    token = openai_api.Account.create(logging=True)
    print(token)

    # with loging:
    # 2023-04-06 21:50:25 INFO __main__ -> register success : '{"id":"51aa0809-3053-44f7-922a...' (2s)
    # 2023-04-06 21:50:25 INFO __main__ -> id : '51aa0809-3053-44f7-922a-2b85d8d07edf'
    # 2023-04-06 21:50:25 INFO __main__ -> token : 'eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...'
    # 2023-04-06 21:50:28 INFO __main__ -> got key : '194158c4-d249-4be0-82c6-5049e869533c' (2s)

    for response in openai_api.StreamingCompletion.create(
        account_data=token, 
        prompt='hello world', 
        model='gpt-4'
        ):
        print(response.choices[0].text, end='')
print("")
