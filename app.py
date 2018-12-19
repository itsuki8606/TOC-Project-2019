from bottle import route, run, request, abort, static_file

from fsm import TocMachine


VERIFY_TOKEN = "F64046127"
machine = TocMachine(
    states=[
        'user',
        'about',
        'introduce',
        'start',
        'select_board',
        'list_all',
        'search',
        'keyword_search',
        'search_article',
        'keyword_article',
        'search_author',
        'keyword_author',
        'search_score',
        'keyword_score'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'about',
            'conditions': 'is_going_to_about'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'introduce',
            'conditions': 'is_going_to_introduce'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'start',
            'conditions': 'is_going_to_start'
        },
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'select_board',
            'conditions': 'is_going_to_select_board'
        },
        {
            'trigger': 'advance',
            'source': 'select_board',
            'dest': 'list_all',
            'conditions': 'is_going_to_list_all'
        },
        {
            'trigger': 'advance',
            'source': 'select_board',
            'dest': 'search',
            'conditions': 'is_going_to_search'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'keyword_search',
            'conditions': 'is_going_to_keyword_search'
        },
        {
            'trigger': 'advance',
            'source': 'select_board',
            'dest': 'search_article',
            'conditions': 'is_going_to_search_article'
        },
        {
            'trigger': 'advance',
            'source': 'search_article',
            'dest': 'keyword_article',
            'conditions': 'is_going_to_keyword_article'
        },
        {
            'trigger': 'advance',
            'source': 'select_board',
            'dest': 'search_author',
            'conditions': 'is_going_to_search_author'
        },
        {
            'trigger': 'advance',
            'source': 'search_author',
            'dest': 'keyword_author',
            'conditions': 'is_going_to_keyword_author'
        },

        {
            'trigger': 'advance',
            'source': 'select_board',
            'dest': 'search_score',
            'conditions': 'is_going_to_search_score'
        },
        {
            'trigger': 'advance',
            'source': 'search_score',
            'dest': 'keyword_score',
            'conditions': 'is_going_to_keyword_score'
        },
        {
            'trigger': 'go_back',
            'source': [
                'about',
                'introduce',
                'list_all',
                'keyword_search',
                'keyword_article',
                'keyword_author',
                'keyword_score'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="localhost", port=5000, debug=True, reloader=True)
