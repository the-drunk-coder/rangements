import sys, copy
# either put scripts in the same folder, or configure the folders below
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *
from MusicalSortingHelpers import *

s_number = "003"
p_number = "04"
s_title = "Einheit-Ordnung"
p_title = "Vier"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Sorted by duration, in descending order, using Quicksort."

einheitsfrontlied_strophe_drei = [
Note(B, none, 3.0, q, "Und"),
Note(E, none, 4.0, q, "weil"),
Note(F, sharp, 4.0, d_e, "der"),
Note(G, none, 4.0, st, "Pro-"),
Note(G, none, 4.0, q, "-let"),
Note(E, none, 4.0, d_e, "ein"),
Note(E, none, 4.0, st, "Pro-"),
Note(F, sharp, 4.0, q, "-let"),
Note(F, sharp, 4.0, h, "ist,"),
Note(B, none, 3.0, q, "drum"),
Note(F, sharp, 4.0, d_e, "kann"),
Note(F, sharp, 4.0, st, "er"),
Note(F, sharp, 4.0, d_e, "sich"),
Note(G, none, 4.0, st, "nur"),
Note(A, none, 4.0, q, "selbst"),
Note(C, none, 5.0, q, "be-"),
Note(B, none, 4.0, d_h, "-frein!"),
Note(B, none, 4.0, q, "Es"),
Note(B, none, 4.0, q, "kann"),
Note(B, none, 4.0, e, "die"),
Note(B, none, 4.0, e, "be-"),
Note(D, none, 5.0, q, "-frei-"),
Note(D, none, 5.0, e, "-ung"),
Note(D, none, 5.0, e, "der"),
Note(C, none, 5.0, q, "Ar-"),
Note(B, none, 4.0, d_e, "-bei-"),
Note(B, none, 4.0, st, "-ter-"),
Note(A, none, 4.0, st, "-klas-"),
Note(A, none, 4.0, st, "-se"),
Rest(e),
Rest(e),
Note(G, none, 4.0, st, "nur"),
Note(G, none, 4.0, st, "das"),
Note(F, sharp, 4.0, q, "Werk"),
Note(F, sharp, 4.0, q, "der"),
Note(B, none, 4.0, q, "Ar-"),
Note(G, none, 4.0, e, "-bei-"),
Note(G, none, 4.0, e, "-ter"),
Note(E, none, 4.0, d_h, "sein!")
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

# sort third verse by duration, descending
einheitsfrontlied_strophe_drei = LilypondTools().set_comparison_type(dur, einheitsfrontlied_strophe_drei)
sorter = QuickSorter(einheitsfrontlied_strophe_drei, direction="desc")
sorter.sort(prune_pivots="True")

# initial padding ...
LilypondTools().match_end(all_voices)
for voice in all_voices:
    voice.add_note(Rest(Decimal('0.75')))

# map reversed chorus to voices                                                 
SortingHelper().quicksort_map_sorter(groups, sorter.sorting_graph)

# match end
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
