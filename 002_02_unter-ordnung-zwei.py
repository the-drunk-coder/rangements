import sys
# either put the scripts to the same folder, or setup below paths ...
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *

s_number = "002"
p_number = "02"
s_title = "Unter-Ordnung"
p_title = "Zwei"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Sorted by duration, in ascending order, using Mergesort. Not time-strict."

# a song from my distant homeland ...
Steigerlied = [
Note(G, none, 4.0, h, "Ins"),
Note(F, sharp, 4.0, q, "Berg-"),
Note(A, none, 4.0, q, "werk"),
Note(G, none, 4.0, h, "ein,"),
Rest(h),
Note(B, none, 4.0, d_q, "wo"),
Note(B, none, 4.0, e, "die"),
Note(A, none, 4.0, q, "Berg-"),
Note(C, none, 5.0, q, "leut'"),
Note(B, none, 4.0, h, "sein,"),
Rest(q),
Note(G, none, 4.0, e, "die"),
Note(A, none, 4.0, e, "da"),
Note(B, none, 4.0, q, "gra-"),
Note(B, none, 4.0, e, "ben"),
Note(B, none, 4.0, e, "das"),
Note(B, none, 4.0, e, "Sil-"),
Note(B, none, 4.0, e, "ber"),
Note(A, none, 4.0, e, "und"),
Note(B, none, 4.0, e, "das"),
Note(C, none, 5.0, q, "Gold"),
Note(A, none, 4.0, d_e, "bei"),
Note(A, none, 4.0, st, "der"),
Note(A, none, 4.0, q, "Nacht,"),
Note(A, none, 4.0, e, "die"),
Note(B, none, 4.0, e, "da"),
Note(C, none, 5.0, q, "gra-"),
Note(E, none, 5.0, e, "ben"),
Note(E, none, 5.0, e, "das"),
Note(E, none, 5.0, e, "Sil-"),
Note(E, none, 5.0, e, "-ber"),
Note(D, none, 5.0, e, "und"),
Note(C, none, 5.0, e, "das"),
Note(D, none, 5.0, q, "Gold"),
Note(B, none, 4.0, d_e, "bei"),
Note(B, none, 4.0, st, "der"),
Note(B, none, 4.0, q, "Nacht,"),
Note(A, none, 4.0, q, "aus"),
Note(G, none, 4.0, h, "Fels-"),
Note(A, none, 4.0, h, "ge-"),
Note(B, none, 4.0, q, "stei-"),
Note(E, none, 5.0, q, "-ei-"),
Note(D, none, 5.0, q, "-n,"),
Note(C, none, 5.0, q, "aus"),
Note(B, none, 4.0, h, "Fels-"),
Note(A, none, 4.0, h, "ge-"),
Note(G, none, 4.0, h, "stein."),
Rest(h)]

# compare by duration, this time
Steigerlied = LilypondTools().set_comparison_type(dur, Steigerlied)

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

for voice in voices:
    LilypondTools().flush_end_to_bar(voice)
    current_node = sorter.sorting_graph.nodes[sorter.step_counter]
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

# generate graph
sorter.sorting_graph.render(s_title + " " + p_title, "Sortiergraph")
