#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015-2020 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

class TrelloWarriorProject:
    def __init__(self, project_name, taskwarrior_project_name, trello_board_name, **kwargs):
        self.project_name = project_name
        self.taskwarrior_project_name = taskwarrior_project_name
        self.trello_board_name = trello_board_name
        self.trello_todo_list = kwargs.get('trello_todo_list', 'To Do')
        self.trello_doing_list = kwargs.get('trello_doing_list', 'Doing')
        self.trello_done_list = kwargs.get('trello_done_list', 'Done')

    def __str__(self):
        return str(self.__dict__)
