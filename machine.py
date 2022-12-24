from fsm import TocMachine


def create_machine():

    machine = TocMachine(
        states=[
            'user',
            'menu',
            'choose_genre',
            'coming_soon_drama',
            'trivia',
            'fsm',
            'option_actor',
            'choose_actor',
            'option_years',
            'choose_years',
            'final',
        ],
        transitions=[
            {'trigger': 'advance', 'source': 'user', 'dest': 'menu', 'conditions': 'is_going_to_menu'},

            {'trigger': 'advance', 'source': 'menu', 'dest': 'choose_genre', 'conditions': 'is_going_to_choose_genre'},
            {'trigger': 'advance', 'source': 'menu', 'dest': 'coming_soon_drama', 'conditions': 'is_going_to_coming_soon_drama'},
            {'trigger': 'advance', 'source': 'menu', 'dest': 'trivia', 'conditions': 'is_going_to_trivia'},
            {'trigger': 'advance', 'source': 'menu', 'dest': 'fsm', 'conditions': 'is_going_to_fsm'},

            {'trigger': 'advance', 'source': 'choose_genre', 'dest': 'option_actor', 'conditions': 'is_going_to_option_actor'}, #確認要不要選演員
            {'trigger': 'advance', 'source': 'option_actor', 'dest': 'choose_actor', 'conditions': 'is_going_to_choose_actor'}, #選演員
            {'trigger': 'advance', 'source': 'option_actor', 'dest': 'final', 'conditions': 'is_going_to_final'}, #直接推薦，不選演員

            {'trigger': 'advance', 'source': 'choose_actor', 'dest': 'option_years', 'conditions': 'is_going_to_option_years'}, #確認要不要選年份
            {'trigger': 'advance', 'source': 'option_years', 'dest': 'choose_years', 'conditions': 'is_going_to_choose_years'}, #選發行年份
            {'trigger': 'advance', 'source': 'option_years', 'dest': 'final', 'conditions': 'is_going_to_final'}, #直接推薦，不選年份

            {'trigger': 'advance', 'source': 'choose_actor', 'dest': 'choose_genre', 'conditions': 'is_going_to_choose_genre'}, #若找不到演員出演的韓劇有此類型
            
            {'trigger': 'advance', 'source': 'choose_years', 'dest': 'final', 'conditions': 'is_going_to_final'}, #直接推薦，不選年份
            {
                'trigger': 'go_back',
                'source': [
                    'coming_soon_drama',
                    'trivia',
                    'fsm',
                    'final',
                ],
                'dest': 'user'
            },
        ],
        initial='user',
        auto_transitions=False,
        show_conditions=True,
    )

    return machine
