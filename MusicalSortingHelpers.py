import sys, copy
# either put scripts in the same folder or configure folders below
# sys.path.append('/path/to/pykopond')
# sys.path.append('/path/to/graph-o-sort')
from LilypondMusicData import *
from GraphingSorters import *

# helper class to map the sorting results to the different voices
class SortingHelper():
    # maps the nodes for quicksort to two groups of either 3 voices.
    def quicksort_map_sorter(self, voice_groups, sorting_graph):
        traversal_list = TraversalTool().topo_trav(sorting_graph)
        reverse_graph = GraphTool().reverse_digraph(sorting_graph)
        print("TRAVERSAL: " + str(traversal_list))
        # copy list ... could use generic node list here, but it doesn't really matter
        nodes_unplayed = list(traversal_list)
        # add original nodes
        for voice in voice_groups[0]:
            voice.add_notes(sorting_graph.nodes[traversal_list[0]].content)
        group_index = 1;
        for node_id in traversal_list:
            # 3 edges means split node
            if len(sorting_graph.edges[node_id]) == 3:
                # find pivot node 
                for succ_id in sorting_graph.edges[node_id]:
                    succ_node = sorting_graph.nodes[succ_id]
                    # make sure pivot node is mapped to center voice
                    if succ_node.meta == "pivot":
                        nodes_unplayed.remove(succ_id)
                        #find smaller and larger successor id
                        smaller_id = len(sorting_graph.nodes)
                        larger_id = 0
                        for non_pivot_succ_id in sorting_graph.edges[node_id]:
                            # holds only true if it's not the pivot node
                            if non_pivot_succ_id != succ_id:
                                if non_pivot_succ_id < smaller_id:
                                    smaller_id = non_pivot_succ_id
                                if non_pivot_succ_id > larger_id:
                                    larger_id = non_pivot_succ_id
                        nodes_unplayed.remove(smaller_id)
                        nodes_unplayed.remove(larger_id)
                        pivot_note = copy.deepcopy(succ_node.content[0])
                        # now find longer of the two other voices, and handle case when size is zero (in that case, add a rest the lenght of the pivot node ...
                        left_duration = LilypondTools().calculate_duration(sorting_graph.nodes[smaller_id].content)
                        right_duration = LilypondTools().calculate_duration(sorting_graph.nodes[larger_id].content)
                        if left_duration >= right_duration:
                            # in this case, both outer nodes are empty
                            if left_duration != Decimal('0.0'):
                                pivot_note.duration = left_duration
                        else:
                            if right_duration != Decimal('0.0'):
                                pivot_note.duration = right_duration
                        voice_groups[group_index][0].add_notes(sorting_graph.nodes[succ_id - 1].content)
                        voice_groups[group_index][1].add_note(pivot_note)
                        voice_groups[group_index][2].add_notes(sorting_graph.nodes[succ_id + 1].content)
                        LilypondTools().match_end(voice_groups[group_index])
            # 1 edge means child node is merged node
            elif len(sorting_graph.edges[node_id]) == 1:
                succ_id = sorting_graph.edges[node_id][0]
                print("SUCC_ID:" + str(succ_id))
                if succ_id in nodes_unplayed:
                    # check if node can be played, or if it has a parent that is yet unplayed
                    # should be only relevant for merged nodes 
                    node_playable = True
                    for edge in reverse_graph.edges[succ_id]:
                        if edge in nodes_unplayed:
                            node_playable = False
                    # only add node if it's playable
                    # if not, it will be added later on ... 
                    if node_playable:
                        nodes_unplayed.remove(succ_id)
                        for voice in voice_groups[group_index]:
                            print("Adding MERGED node " + str(succ_id) +" to voice") 
                            voice.add_notes(sorting_graph.nodes[succ_id].content)
            print("NODES UNPLAYED" + str(nodes_unplayed))
            group_index = (group_index + 1) % 2
        
                    
