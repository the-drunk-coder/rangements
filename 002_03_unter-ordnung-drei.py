import sys
# either put the scripts to the same folder, or setup below paths ...
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *

s_number = "002"
p_number = "03"
s_title = "Unter-Ordnung"
p_title = "Drei"
p_composer = "Niklas Reppel, 2014"
p_attribs = "Un-sorted by pitch, in descending order, using Mergesort. Not time-strict."

# a song from my distant homeland ...
Steigerlied = [
Note(G, none, 4.0, h, "Die"),
Note(F, sharp, 4.0, q, "Berg-"),
Note(A, none, 4.0, q, "-leut'"),
Note(G, none, 4.0, h, "sein's"),
Rest(h),
Note(B, none, 4.0, h, "kreuz-"),
Note(A, none, 4.0, q, "-bra-"),
Note(C, none, 5.0, q, "-ve"),
Note(B, none, 4.0, h, "Leut."),
Rest(q),
Note(G, none, 4.0, e, "denn"),
Note(A, none, 4.0, e, "sie"),
Note(B, none, 4.0, q, "tra-"),
Note(B, none, 4.0, e, "-gen"),
Note(B, none, 4.0, e, "das"),
Note(B, none, 4.0, e, "Le-"),
Note(B, none, 4.0, e, "-der"),
Note(A, none, 4.0, e, "vor"),
Note(B, none, 4.0, e, "dem"),
Note(C, none, 5.0, q, "Arsch"),
Note(A, none, 4.0, d_e, "bei"),
Note(A, none, 4.0, st, "der"),
Note(A, none, 4.0, q, "Nacht,"),
Note(A, none, 4.0, e, "denn"),
Note(B, none, 4.0, e, "sie"),
Note(C, none, 5.0, q, "tra-"),
Note(E, none, 5.0, e, "-gen"),
Note(E, none, 5.0, e, "das"),
Note(E, none, 5.0, e, "Le-"),
Note(E, none, 5.0, e, "-der"),
Note(C, none, 5.0, e, "vor"),
Note(B, none, 4.0, e, "dem"),
Note(D, none, 5.0, q, "Arsch"),
Note(B, none, 4.0, d_e, "bei"),
Note(B, none, 4.0, st, "der"),
Note(B, none, 4.0, q, "Nacht"),
Note(A, none, 4.0, q, "und"),
Note(G, none, 4.0, h, "sau-"),
Note(A, none, 4.0, h, "-fen"),
Note(B, none, 4.0, q, "Schna-"),
Note(E, none, 5.0, q, "-a-"),
Note(D, none, 5.0, q, "-aps,"),
Note(C, none, 5.0, q, "und"),
Note(B, none, 4.0, h, "Sau-"),
Note(A, none, 4.0, h, "-fen"),
Note(G, none, 4.0, h, "Schnaps"),
Rest(h)]

# sort the song using mergesort
sorter = MergeSorter(Steigerlied, "desc")
sorter.sort()

# a quartet ...
voices =[
LilypondVoice(full_name="Core 1", short_name="eins", contains_lyrics=True),
LilypondVoice(full_name="Core 2", short_name="zwei", contains_lyrics=True),
LilypondVoice(full_name="Core 3", short_name="drei", contains_lyrics=True),
LilypondVoice(full_name="Core 4", short_name="vier", contains_lyrics=True),
]

# this time, start with the sorted notes 
sorted_node = sorter.sorting_graph.nodes[sorter.step_counter]
for voice in voices:
    voice.add_notes(sorted_node.content)

# spread onset of voices, first 4 sorting nodes
for node_ptr in range(sorter.step_counter - 1 , 0, -1):
    current_node = sorter.sorting_graph.nodes[node_ptr]
    voices[node_ptr % 4].add_notes(current_node.content)

LilypondTools().match_end(voices)

#flush end
for voice in voices:
    LilypondTools().flush_end_to_bar(voice)

# add 'unsorted' notes to first voice
voices[0].add_notes(sorter.sorting_graph.nodes[0].content)

rest_padding = LilypondTools().calculate_duration(sorter.sorting_graph.nodes[0].content)

# pad other voices
for i in range(1,4):
    voices[i].add_note(Rest(rest_padding))

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
sorter.sorting_graph.render(s_title + p_title, "Mergesort example")

