#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015-2020 Óscar García Amor <ogarcia@connectical.com>
#
# Distributed under terms of the GNU GPLv3 license.

from trello import TrelloClient as Client
from trello.exceptions import ResourceUnavailable

import logging

logger = logging.getLogger(__name__)

class TrelloClient:
    def __init__(self, api_key, api_secret, token, token_secret):
        self.trello_client = Client(api_key=api_key, api_secret=api_secret, token=token, token_secret=token_secret)

    def get_trello_board(self, board_name):
        """
        Get a open Trello board from name, if it does not exist create it

        :param board_name: the board name
        :return: a Tello board
        :rtype: Trello board object
        """
        for trello_board in self.trello_client.list_boards(board_filter='open'):
            if trello_board.name == board_name and not trello_board.closed:
                logger.debug('Trello board {} found'.format(board_name))
                return trello_board
        logger.debug('Creating Trello board {}'.format(board_name))
        return self.trello_client.add_board(board_name)

    def get_trello_lists(self, board_name):
        """
        Get the open lists of a Trello board

        :param board_name: the board name
        :return: a list of Trello list objects
        :rtype: list
        """
        return self.get_trello_board(board_name).open_lists()

    def get_trello_list(self, board_name, trello_lists, list_name):
        """
        Get a Trello list from list name, if it does not exist create it

        :param board_name: the board name
        :param trello_lists: list of Trello lists objects
        :param list_name: the list name
        :return: a Tello list
        :rtype: Trello list object
        """
        for trello_list in trello_lists:
            if trello_list.name == list_name:
                logger.debug('Trello list {} found'.format(list_name))
                return trello_list
        logger.debug('Creating Trello list {}'.format(list_name))
        trello_list = self.get_trello_board(board_name).add_list(list_name)
        trello_lists.append(trello_list) # Update trello_lists with new list
        return trello_list

    def get_trello_cards_dict(self, trello_lists):
        """
        Get all cards of a list of Trello lists in a dictionary

        :param trello_lists: list of Trello lists
        :return: a dict with Cards
        :rtype: dict
        """
        trello_cards_dict = {}
        for trello_list in trello_lists:
            logger.debug('Getting Trello cards of list {}'.format(trello_list.name))
            trello_cards_dict[trello_list.name] = trello_list.list_cards()
        return trello_cards_dict

    def delete_trello_card(self, trello_card_id):
        """
        Delete (forever) a Trello card by ID

        :param trello_card_id: ID of Trello card
        """
        try:
            self.trello_client.get_card(trello_card_id).delete()
        except ResourceUnavailable:
            logger.warning('Cannot find Trello card with ID {} deleted in Task Warrior. Maybe you also deleted it in Trello?'.format(trello_card_id))
