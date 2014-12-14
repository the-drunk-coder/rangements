import sys, copy
# either put scripts in the same folder, or configure the folders below
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *
from MusicalSortingHelpers import *
                           
s_number = "003"
p_number = "02"
s_title = "Einheit-Ordnung"
p_title = "Zwei"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Sorted by pitch, in descending order, using Quicksort."

# this time the upbeat is included, leading to an extremely bad case for the quicksort algorithm,
# which in return leads to a musically more interesting result ... 
einheitsfrontlied_strophe_zwei = [
Rest(d_h),
Note(B, none, 3.0, q, "Und"),
Note(E, none, 4.0, q, "weil"),
Note(F, sharp, 4.0, q, "der"),
Note(G, none, 4.0, q, "Mensch"),
Note(E, none, 4.0, q, "ein"),
Note(F, sharp, 4.0, q, "Mensch"),
Note(F, sharp, 4.0, h, "ist,"),
Note(B, none, 3.0, q, "drum"),
Note(F, sharp, 4.0, e, "hat"),
Note(F, sharp, 4.0, e, "er"),
Note(F, sharp, 4.0, e, "Stie-"),
Note(G, none, 4.0, e, "-fel"),
Note(A, none, 4.0, e, "im"),
Note(A, none, 4.0, e, "Ge-"),
Note(F, sharp, 4.0, e, "-sicht"),
Note(C, none, 5.0, e, "nicht"),
Note(B, none, 4.0, d_h, "gern!"),
Note(B, none, 4.0, q, "Er"),
Note(B, none, 4.0, q, "will"),
Note(B, none, 4.0, e, "unt-"),
Note(B, none, 4.0, e, "-ter"),
Note(D, none, 5.0, q, "sich"),
Note(D, none, 5.0, e, "kei-"),
Note(D, none, 5.0, e, "-ne"),
Note(C, none, 5.0, q, "Skla-"),
Note(B, none, 4.0, q, "-ven"),
Note(A, none, 4.0, q, "sehn,"),
Note(G, none, 4.0, q, "und"),
Note(F, sharp, 4.0, q, "ü-"),
Note(F, sharp, 4.0, q, "-ber"),
Note(B, none, 4.0, q, "sich"),
Note(G, none, 4.0, e, "kei-"),
Note(G, none, 4.0, e, "-ne"),
Note(E, none, 4.0, d_h, "Herrn!"),
Rest(q)
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

# sort by pitch, descending
sorter = QuickSorter(einheitsfrontlied_strophe_zwei, direction="desc")

# sort second verse
sorter.sort(prune_pivots=True)

sorter.sorting_graph.render(s_title + p_title, "Sortiergraph", render="all")

# map second verse
SortingHelper().quicksort_map_sorter(groups, sorter.sorting_graph)

# padding ...
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
