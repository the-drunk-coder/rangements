import sys, copy
# either put scripts in the same folder, or configure the folders below
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *
from MusicalSortingHelpers import *

s_number = "003"
p_number = "05"
s_title = "Einheit-Ordnung"
p_title = "Fünf"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Un-sorted by duration, in descending order, using Quicksort."

einheitsfrontlied_refrain = [
Note(A, none, 4.0, q, "Drum"),
Note(E, none, 4.0, e, "links,"),
Rest(e),
Note(E, none, 4.0, q, "zwei,"),
Note(E, none, 4.0, q, "drei!"),
Note(C, none, 5.0, q, "Drum"),
Note(F, sharp, 4.0, e, "links,"),
Rest(e),
Note(F, sharp, 4.0, q, "zwei,"),
Note(F, sharp, 4.0, q, "drei!"),
Note(E, none, 4.0, e, "Wo"),
Note(E, none, 4.0, e, "dein"),
Note(B, none, 4.0, d_q, "Platz,"),
Note(B, none, 4.0, e, "Ge-"),
Note(D, none, 5.0, e, "-nos-"),
Note(D, none, 5.0, d_q, "-se,"),
Note(C, none, 5.0, q, "ist!"),
Rest(h),
Note(E, none, 4.0, e, "Reih'"),
Note(E, none, 4.0, e, "dich"),
Note(C, none, 5.0, q, "ein"),
Note(C, none, 5.0, d_e, "in"),
Note(C, none, 5.0, st, "die"),
Note(C, none, 5.0, q, "Ar-"),
Note(B, none, 4.0, d_e, "-bei-"),
Note(A, sharp, 4.0, st, "-ter-"),
Note(B, none, 4.0, q, "-ein-"),
Note(G, none, 4.0, q, "-heits-"),
Note(E, none, 4.0, q, "-front,"),
Note(E, none, 4.0, e, "weil"),
Note(G, none, 4.0, e, "du"),
Note(B, none, 4.0, q, "auch"),
Note(A, none, 4.0, q, "ein"),
Note(G, none, 4.0, q, "Ar-"),
Note(F, none, 4.0, e, "-bei-"),
Note(F, none, 4.0, e, "-ter"),
Note(E, none, 4.0, q, "bist!")
]

# two groups of voices
groups=[
[
LilypondVoice(full_name="eins_links", short_name="eins_l", contains_lyrics=True),
LilypondVoice(full_name="eins_pivot", short_name="eins_p", clef="bass", contains_lyrics=True),
LilypondVoice(full_name="eins_rechts", short_name="eins_r", contains_lyrics=True)
],
[
LilypondVoice(full_name="zwei_links", short_name="zwei_l", contains_lyrics=True),
LilypondVoice(full_name="zwei_pivot", short_name="zwei_p", clef="bass", contains_lyrics=True),
LilypondVoice(full_name="zwei_rechts", short_name="zwei_r", contains_lyrics=True)
]
]

# make all voices iterable for certain purposes (see below)
all_voices = []
all_voices.extend(groups[0])
all_voices.extend(groups[1])

# sort chorus by duration, descending
einheitsfrontlied_refrain = LilypondTools().set_comparison_type(dur, einheitsfrontlied_refrain)
sorter = QuickSorter(einheitsfrontlied_refrain, direction="desc")
sorter.sort()

# reverse order, prune pivots
chorus_two_reverse = GraphTool().reverse_digraph(sorter.sorting_graph)
chorus_two_reverse = SorterTool().quicksort_prune_pivots(chorus_two_reverse)

# padding initial padding, to keep some kind of upbeat
for voice in all_voices:
    voice.add_note(Rest(Decimal('0.75')))

SortingHelper().quicksort_map_sorter(groups, chorus_two_reverse)

LilypondTools().match_end(all_voices)
for voice in all_voices:
    LilypondTools().flush_end_to_bar(voice)
    
# transpose pivot voices one octave down
groups[0][1].notes = LilypondTools().octave_down(groups[0][1].notes)
groups[1][1].notes = LilypondTools().octave_down(groups[1][1].notes)

# generate score-, group- & individual voices
score_complete = LilypondScore(series_number = s_number, piece_number=p_number, series_title = s_title, piece_title=p_title, composer=p_composer, subtitle="Partitur Komplett", subsubtitle=p_attribs)
score_complete.add_voices(groups[0])
score_complete.add_voices(groups[1])
score_complete.output_pdf()

score_group_1 = LilypondScore(series_number = s_number, piece_number=p_number, series_title = s_title, piece_title=p_title, composer=p_composer, subtitle="Partitur Gruppe 1", subsubtitle=p_attribs)
score_group_1.add_voices(groups[0])
score_group_1.output_pdf()

score_group_2 = LilypondScore(series_number = s_number, piece_number=p_number, series_title = s_title, piece_title=p_title, composer=p_composer, subtitle="Partitur Gruppe 2", subsubtitle=p_attribs)
score_group_2.add_voices(groups[1])
score_group_2.output_pdf()

for i in range(0, len(all_voices)):
    voice_score = LilypondScore(series_number = s_number, piece_number=p_number, series_title = s_title, piece_title=p_title, composer=p_composer, subtitle="Stimme " + str((i+1)), subsubtitle=p_attribs)
    voice_score.add_voice(all_voices[i])
    voice_score.output_pdf()
 
