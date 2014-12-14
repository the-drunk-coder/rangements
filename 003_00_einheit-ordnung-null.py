import sys, copy
# either put scripts in the same folder, or configure the folders below
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *
from MusicalSortingHelpers import *

s_number = "003"
p_number = "00"
s_title = "Einheit-Ordnung"
p_title = "Null"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Un-sorted by duration, in ascending order, using Quicksort."

einheitsfrontlied_strophe_eins = [
Note(B, none, 3.0, q, "Und"),
Note(E, none, 4.0, q, "weil"),
Note(F, sharp, 4.0, q, "der"),
Note(G, none, 4.0, q, "Mensch"),
Note(E, none, 4.0, q, "ein"),
Note(F, sharp, 4.0, q, "Mensch"),
Note(F, sharp, 4.0, h, "ist,"),
Note(B, none, 3.0, q, "drum"),
Note(F, sharp, 4.0, e, "braucht"),
Note(F, sharp, 4.0, e, "er"),
Note(F, sharp, 4.0, e, "was"),
Note(G, none, 4.0, e, "zum"),
Note(A, none, 4.0, e, "Es-"),
Note(A, none, 4.0, e, "-sen,"),
Note(F, sharp, 4.0, e, "bit-"),
Note(C, none, 5.0, e, "-te"),
Note(B, none, 4.0, d_h, "sehr!"),
Note(B, none, 4.0, q, "Es"),
Note(B, none, 4.0, q, "macht"),
Note(B, none, 4.0, q, "ihn"),
Note(D, none, 5.0, d_q, "ein"),
Note(D, none, 5.0, e, "Ge-"),
Note(C, none, 5.0, q, "-schwätz"),
Note(B, none, 4.0, q, "nicht"),
Note(A, none, 4.0, q, "satt,"),
Note(G, none, 4.0, q, "das"),
Note(F, sharp, 4.0, q, "schafft"),
Note(F, sharp, 4.0, q, "kein"),
Note(B, none, 4.0, e, "Es-"),
Note(G, none, 4.0, d_q, "-sen,"),
Note(E, none, 4.0, q, "her")
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

# the sorters
# sort first verse by duration
einheitsfrontlied_strophe_eins = LilypondTools().set_comparison_type(dur, einheitsfrontlied_strophe_eins)
sorter = QuickSorter(einheitsfrontlied_strophe_eins)

# sort first verse
sorter.sort()

# reverse sorting graph of first verse, then prune pivots to make topological sorting more meaningful
verse_one_reverse_duration = GraphTool().reverse_digraph(sorter.sorting_graph)
verse_one_reverse_duration = SorterTool().quicksort_prune_pivots(verse_one_reverse_duration)

# render first graph
verse_one_reverse_duration.render("einheit_strophe_1_rev_prune", "sortiergraph", render="all")

# padding initial padding, to keep some kind of upbeat
for voice in all_voices:
    voice.add_note(Rest(Decimal('0.75')))

# map first verse to voices
SortingHelper().quicksort_map_sorter(groups, verse_one_reverse_duration)

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
    


