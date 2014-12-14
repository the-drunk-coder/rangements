import sys
# either put the scripts to the same folder, or setup below paths ...
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *

s_number = "002"
p_number = "00"
s_title = "Unter-Ordnung"
p_title = "Null"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Sorted by pitch, in ascending order, using Mergesort. Not time-strict."

# a song from my distant homeland ...
Steigerlied = [
Note(G, none, 4.0, h, "Glück"),
Note(F, sharp, 4.0, q, "auf"),
Note(A, none, 4.0, q, "Glück"),
Note(G, none, 4.0, h, "auf"),
Rest(h),
Note(B, none, 4.0, h, "der"),
Note(A, none, 4.0, q, "Stei-"),
Note(C, none, 5.0, q, "ger"),
Note(B, none, 4.0, h, "kommt"),
Rest(q),
Note(G, none, 4.0, e, "und"),
Note(A, none, 4.0, e, "er"),
Note(B, none, 4.0, q, "hat"),
Note(B, none, 4.0, q, "sein"),
Note(B, none, 4.0, q, "hel-"),
Note(A, none, 4.0, e, "-le-"),
Note(B, none, 4.0, e, "-es-"),
Note(C, none, 5.0, q, "Licht"),
Note(A, none, 4.0, d_e, "bei"),
Note(A, none, 4.0, st, "der"),
Note(A, none, 4.0, q, "Nacht,"),
Note(A, none, 4.0, e, "und"),
Note(B, none, 4.0, e, "er"),
Note(C, none, 5.0, q, "hat"),
Note(E, none, 5.0, q, "sein"),
Note(E, none, 5.0, q, "hel"),
Note(C, none, 5.0, e, "-le-"),
Note(B, none, 4.0, e, "-es"),
Note(D, none, 5.0, q, "Licht"),
Note(B, none, 4.0, d_e, "bei"),
Note(B, none, 4.0, st, "der"),
Note(B, none, 4.0, q, "Nacht,"),
Note(A, none, 4.0, q, "schon"),
Note(G, none, 4.0, h, "an"),
Note(A, none, 4.0, h, "ge"),
Note(B, none, 4.0, q, "zü-"),
Note(E, none, 5.0, q, "-ü-"),
Note(D, none, 5.0, q, "-ündt´,"),
Note(C, none, 5.0, q, "schon"),
Note(B, none, 4.0, h, "an"),
Note(A, none, 4.0, h, "ge"),
Note(G, none, 4.0, h, "zündt´."),
Rest(h)]

# sort the song using mergesort
sorter = MergeSorter(Steigerlied)
sorter.sort()

# a quartet ...
voices =[
LilypondVoice(full_name="Core 1", short_name="eins", contains_lyrics=True),
LilypondVoice(full_name="Core 2", short_name="zwei", contains_lyrics=True),
LilypondVoice(full_name="Core 3", short_name="drei", contains_lyrics=True),
LilypondVoice(full_name="Core 4", short_name="vier", contains_lyrics=True),
]

# spread onset of voices, first 4 sorting nodes
for node_ptr in range(0,4):
    current_node = sorter.sorting_graph.nodes[node_ptr]
    voices[node_ptr].add_notes(current_node.content)
    rest_padding = LilypondTools().calculate_duration(current_node.content)
    for j in range(node_ptr + 1, 4):
        voices[j].add_note(Rest(rest_padding))

# distribute nodes to voices
for node_ptr in range(4, sorter.step_counter - 1):
    current_node = sorter.sorting_graph.nodes[node_ptr]
    voices[node_ptr % 4].add_notes(current_node.content)

LilypondTools().match_end(voices)

current_node = sorter.sorting_graph.nodes[sorter.step_counter]
for voice in voices:
    LilypondTools().flush_end_to_bar(voice)
    voice.add_notes(current_node.content)

# generate lilypond scores
score = LilypondScore(series_number=s_number, piece_number=p_number, series_title=s_title, piece_title=p_title, composer=p_composer, subtitle="Partitur", subsubtitle=p_attribs)
score.add_voices(voices)
score.output_pdf()

score_v1 = LilypondScore(series_number=s_number, piece_number=p_number, series_title=s_title, piece_title=p_title, composer=p_composer, subtitle="Stimme Eins", subsubtitle=p_attribs)
score_v1.add_voice(voices[0])
score_v1.output_pdf()

score_v2 = LilypondScore(series_number=s_number, piece_number=p_number, series_title=s_title, piece_title=p_title, composer=p_composer, subtitle="Stimme Zwei", subsubtitle=p_attribs)
score_v2.add_voice(voices[1])
score_v2.output_pdf()

score_v3 = LilypondScore(series_number=s_number, piece_number=p_number, series_title=s_title, piece_title=p_title, composer=p_composer, subtitle="Stimme Drei", subsubtitle=p_attribs)
score_v3.add_voice(voices[2])
score_v3.output_pdf()

score_v4 = LilypondScore(series_number=s_number, piece_number=p_number, series_title=s_title, piece_title=p_title, composer=p_composer, subtitle="Stimme Vier", subsubtitle=p_attribs)
score_v4.add_voice(voices[3])
score_v4.output_pdf()

# Generate Graph
sorter.sorting_graph.render(s_title + "_" + p_title, "Sortiergraph")
