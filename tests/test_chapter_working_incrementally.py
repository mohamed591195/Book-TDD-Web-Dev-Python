#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from book_tester import (
    ChapterTest,
    Command,
)

class Chapter7Test(ChapterTest):
    chapter_name = 'chapter_working_incrementally'
    previous_chapter = 'chapter_explicit_waits_1'

    def test_listings_and_commands_and_output(self):
        self.parse_listings()

        # sanity checks
        self.assertEqual(self.listings[0].type, 'code listing currentcontents')
        self.assertEqual(self.listings[1].type, 'output')

        # skips
        self.skip_with_check(40, 'should show 4 changed files') # git
        self.skip_with_check(45, 'add a message summarising') # git
        self.skip_with_check(63, '5 changed files') # git
        self.skip_with_check(65, 'forms x2') # git
        self.skip_with_check(92, '3 changed files') # git
        touch_pos = 33
        touch = self.listings[touch_pos]
        assert 'touch' in touch

        # other prep
        self.start_with_checkout()
        self.run_command(Command('python3 manage.py migrate --noinput'))

        # hack fast-forward
        skip = False
        if skip:
            self.pos = 106
            self.sourcetree.run_command('git checkout {}'.format(
                self.sourcetree.get_commit_spec('ch07l036-1')
            ))

        while self.pos < touch_pos:
            print(self.pos)
            self.recognise_listing_and_process_it()


        # special-case: we have a touch followed by some output.
        # just do this one manually
        if self.pos < touch_pos + 1:
            output = self.run_command(touch)
            self.assertFalse(output)
            touch.was_checked = True
            self.pos = touch_pos + 1

        while self.pos < len(self.listings):
            print(self.pos)
            self.recognise_listing_and_process_it()

        self.assert_all_listings_checked(self.listings)
        self.check_final_diff(ignore=["moves", "Generated by Django 2.1"])


if __name__ == '__main__':
    unittest.main()
