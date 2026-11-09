import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game
from cabinet import CabinetStore

class InitialsQA(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=Path.cwd())
        self.store=CabinetStore(self.temp.name)
        self.app=game.App(cabinet=self.store,simulate_controllers=True)
        self.store.settings['fill_bots']=False
        game.pg.event.clear()
    def tearDown(self):game.pg.quit();self.temp.cleanup()
    def key(self,key,text=''):
        game.pg.event.post(game.pg.event.Event(game.pg.KEYDOWN,key=key,unicode=text))
        self.app.events()
    def finish(self,count):
        self.app.count=count;self.app.start()
        for p in self.app.match.players:p.score=1234
        self.app.match.over=True
    def test_two_and_eight_rows_save_and_reload(self):
        for count in (2,8):
            self.finish(count);token=self.app.session_id
            self.key(game.pg.K_n,'n');self.assertIsNotNone(self.app.name_entry)
            for i in range(count):
                for letter in 'XYZ':self.key(ord(letter.lower()),letter.lower())
                self.key(game.pg.K_RETURN)
            self.assertIsNone(self.app.name_entry)
            rows=[r for r in CabinetStore(self.temp.name).high_scores if r.get('session')==token]
            self.assertEqual(len(rows),count);self.assertTrue(all(r['name']=='XYZ' for r in rows))
    def test_duplicate_scores_other_sessions_and_legacy_are_untouched(self):
        self.store.record_rows([{'player_id':1,'score':1234}], 'old')
        self.store.high_scores.append({'name':'OLD','player_id':1,'score':1234,'time':0})
        self.store.save();self.finish(1);token=self.app.session_id;self.key(game.pg.K_n,'n')
        for letter in 'NEW':self.key(ord(letter.lower()),letter)
        self.key(game.pg.K_RETURN)
        rows=CabinetStore(self.temp.name).high_scores
        self.assertEqual(next(r['name'] for r in rows if r.get('session')==token),'NEW')
        self.assertEqual(next(r['name'] for r in rows if r.get('session')=='old'),'P1')
        self.assertEqual(next(r['name'] for r in rows if r.get('session') is None),'OLD')
    def test_failed_rename_rolls_back_memory_disk_and_allows_retry(self):
        self.finish(1);self.key(game.pg.K_n,'n');before=self.store.path.read_text()
        for letter in 'ABC':self.key(ord(letter.lower()),letter)
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):self.key(game.pg.K_RETURN)
        self.assertIsNotNone(self.app.name_entry);self.assertTrue(self.app.name_entry['error'])
        self.assertEqual(self.store.high_scores[0]['name'],'P1')
        self.assertEqual(self.store.path.read_text(),before)
        self.assertEqual(CabinetStore(self.temp.name).high_scores[0]['name'],'P1')
        self.key(game.pg.K_RETURN);self.assertEqual(self.store.high_scores[0]['name'],'ABC')
    def test_immediate_restart_and_pending_results_remain_safe(self):
        self.finish(2);token=self.app.session_id
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):
            self.key(game.pg.K_n,'n');self.assertIsNone(self.app.name_entry)
            self.assertIn('not saved',self.app.status_notice)
            self.key(game.pg.K_RETURN)
        self.assertFalse(self.app.match.over);self.assertTrue(self.app.pending_results)
        self.app.save_result();self.assertFalse(self.app.pending_results)
        self.assertEqual(sum(r.get('session')==token for r in self.store.high_scores),2)
    def test_cancel_arrows_backspace_and_explicit_editor_blocks_restart(self):
        self.finish(1);self.key(game.pg.K_n,'n');token=self.app.session_id
        self.key(game.pg.K_F3);self.assertEqual(self.app.session_id,token)
        self.key(game.pg.K_DOWN);self.assertEqual(self.app.name_entry['letters'][0],'Z')
        self.key(game.pg.K_RIGHT);self.key(game.pg.K_UP)
        self.assertEqual(self.app.name_entry['letters'],list('ZBA'))
        self.key(game.pg.K_BACKSPACE);self.assertEqual(self.app.name_entry['letters'],list('ABA'))
        self.key(game.pg.K_ESCAPE);self.assertIsNone(self.app.name_entry)
        self.assertEqual(self.store.high_scores[0]['name'],'P1')
        self.key(game.pg.K_F3);self.assertNotEqual(self.app.session_id,token)
    def test_no_qualifying_rows_and_bad_initials(self):
        self.store.record_rows([{'player_id':1,'score':99999} for _ in range(20)],'old')
        self.finish(1);self.key(game.pg.K_n,'n')
        self.assertIsNone(self.app.name_entry);self.assertIn('No score',self.app.status_notice)
        for value in ('AB','ABCD','éAB','A B',None):
            with self.assertRaises(ValueError):self.store.rename_score('old',1,value)
    def test_partial_qualification_and_cancel_preserves_already_saved_name(self):
        self.store.record_rows([{'player_id':1,'score':99999} for _ in range(18)],'old')
        self.finish(8);token=self.app.session_id;self.key(game.pg.K_n,'n')
        self.assertEqual(len(self.app.name_entry['rows']),2)
        for letter in 'WIN':self.key(ord(letter.lower()),letter)
        self.key(game.pg.K_RETURN);self.key(game.pg.K_z,'z');self.key(game.pg.K_ESCAPE)
        rows=[r for r in CabinetStore(self.temp.name).high_scores if r.get('session')==token]
        self.assertEqual([r['name'] for r in rows],['WIN','P2'])
    def test_n_during_play_keeps_keyboard_control_and_cannot_open_editor(self):
        self.app.count=8;self.app.start()
        self.key(game.pg.K_n,'n')
        self.assertIsNone(self.app.name_entry)
        self.assertEqual(self.app.match.players[6].wanted,(1,0))
    def test_cancel_does_not_rename_even_after_draft_write_failure(self):
        self.finish(1);self.key(game.pg.K_n,'n')
        for letter in 'BAD':self.key(ord(letter.lower()),letter)
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):self.key(game.pg.K_RETURN)
        self.key(game.pg.K_ESCAPE)
        self.assertEqual(CabinetStore(self.temp.name).high_scores[0]['name'],'P1')

    def test_editor_render_text_fits_panel(self):
        self.finish(8);self.key(game.pg.K_n,'n');rects=[];original=self.app.text
        def capture(text,x,y,color=(224,234,247),font=None):
            if 155<=y<=565 and 190<=x<=1090:
                rects.append((str(text),(font or self.app.font).render(str(text),True,color).get_rect(topleft=(x,y))))
            return original(text,x,y,color,font)
        with patch.object(self.app,'text',capture):self.app.draw(0)
        editor=[(text,rect) for text,rect in rects if 'INITIALS' in text or 'draft' in text or 'Entry' in text]
        self.assertEqual(len(editor),3)
        for text,rect in editor:self.assertTrue(game.pg.Rect(190,155,900,410).contains(rect),(text,rect))

if __name__=='__main__':unittest.main(verbosity=2)
