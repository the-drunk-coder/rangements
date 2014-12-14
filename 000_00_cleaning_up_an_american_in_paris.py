 # Cleaning up an American in Paris (for Tom Johnson)
 # Ein Amerikaner in Paris aufräumen (für Tom Johnson)
 #
 # (source code)
 #
 # by Niklas Reppel
 #
 # Copyright 2009 Niklas Reppel
 #
 # nik@parkellipsen.de
 #
 # http://www.parkellipsen.de/rangement
 #
 # --
 #
 # This is the generating source code for my piece "Cleaning Up An American In Paris" 
 # 
 # =====================
 # Some technical notes: (for musical notes, please read the introduction for the piece) 
 # =====================
 #
 # In this case, Notes are represented by a tuple, with the first value representing the pitch 
 # and the second value representing the length. 
 # The pitch value is (in this case) an integer, where 1 is "c,," going upwards in half tone steps, so that 2 is "cis,," etc. 
 # The length value is the number of eigth-notes so that 1 means the note is one eigth note long, 4 means a half note etc. 
 # A rest ist represented by pitch value zero.
 # So, you can represent a melody as an array of tuples (as seen below).
 # 
 # The orignial mergesort implementation was recieved from:
 # 
 # Retrieved from: http://en.literateprograms.org/Merge_sort_(Python)?oldid=11584
 #
 # To re-generate the score and individual voices, you'll need lilypond installed on your system, in addition to python3, of course.
 # If you want the package to be generated, you'll need zip installed as well.
 # 
 # Furthermore, this little script has only been tested on Linux. If you're working on a different OS, you'll might need to adapt some lines. 
 #
 # =========================
 # Revision: December 14, 2014
 # =========================
 # - Code has been updated to python3 
 # - from now on, no additional manual work should be necessary, this skript will generate all files
import os

foldername = "000_cleaning_up_an_american_in_paris/"

voice_one_file = """ 
\\version \"2.18.2\"

{0}

\\header {{
       title = \"Ein Amerikaner in Paris aufräumen\"
       dedication = \"for Tom Johnson\"
       subtitle = \"Cleaning up an American in Paris\"
       subsubtitle= \"Voice A\"
       meter = \"ca. 140 bpm\"
       composer = \"Niklas Reppel, 2009\"

       copyright= \\markup \\teeny {{Published under Creative Commons by-sa-nc 3.0 (see included textfile for details)}}
      }}

\\score {{
 \\new GrandStaff {{
      <<
      \\new Staff  \\Stimmeeins
      >>
  }}
}} 
"""

voice_two_file = """ 
\\version \"2.18.2\"

{0}

\\header {{
       title = \"Ein Amerikaner in Paris aufräumen\"
       dedication = \"for Tom Johnson\"
       subtitle = \"Cleaning up an American in Paris\"
       subsubtitle= \"Voice B\"
       meter = \"ca. 140 bpm\"
       composer = \"Niklas Reppel, 2009\"

       copyright= \\markup \\teeny {{Published under Creative Commons by-sa-nc 3.0 (see included textfile for details)}}
      }}

\\score {{
 \\new GrandStaff {{
      <<
      \\new Staff  \\Stimmezwei
      >>
  }}
}} 
"""

score_file = """ 
\\version \"2.18.2\"

{0}
{1}

\\header {{
       title = \"Ein Amerikaner in Paris aufräumen\"
       dedication = \"for Tom Johnson\"
       subtitle = \"Cleaning up an American in Paris\"
       subsubtitle= \"Score\"
       meter = \"ca. 140 bpm\"
       composer = \"Niklas Reppel, 2009\"

       copyright= \\markup \\teeny {{Published under Creative Commons by-sa-nc 3.0 (see included textfile for details)}}
      }}

\\score {{
 \\new GrandStaff {{
      <<
      \\new Staff  \\Stimmeeins
      \\new Staff  \\Stimmezwei
      >>
  }}
}} 
"""
  
class sorter():
    unsorted = []
    sorted_result = []
    voiceone = "Stimmeeins = { \\clef treble \\time 4/4 "
    voicetwo = "Stimmezwei = { \\clef treble \\time 4/4 "
    mergedest = 1;
    restdest = 2;
    cutdest = 1;
    cutrestdest = 2;
    def __init__(self, notes):
       self.unsorted = notes
       self.resttakt_eins = 8
       self.resttakt_zwei = 8
       self.notify(self.unsorted, 1, False, False)
       self.notify(self.unsorted, 2, False, False)
       self.sorted_result = self.mergesort(self.mergesort(self.unsorted, 1),0)#1st arg: list to be sorted 2nd arg: see below
       self.notify(self.sorted_result, 1, False, False)
       self.notify(self.sorted_result, 2, False, False)
 
    def merge(self, left, right, value): #value 1: sort by length value 0: sort by pitch
         result = []
         i = 0
         j = 0
         swap = 0;
         
         while(i < len(left) and j < len(right)):
             if (left[i][value] <= right[j][value]):
                 result.append(left[i])
                 i = i + 1
             else:
                 result.append(right[j])
                 j = j + 1
 
         result += left[i:]
         result += right[j:]
         self.notify(result, self.mergedest, False, True)
         self.notify(result, self.restdest, True, False)
         swap = self.mergedest
         self.mergedest = self.restdest
         self.restdest = swap
         return result
 
    def mergesort(self, list,value):
        swap = 0
        if len(list) < 2:
            self.notify(list, self.cutdest, False, False)
            self.notify(list, self.cutrestdest, True, False)
            swap = self.cutdest
            self.cutdest = self.cutrestdest
            self.cutrestdest = swap
            return list
        else:
            middle = len(list) // 2
            if middle > 1:
                self.notify(list[:middle], 1, False, False)
                self.notify(list[:middle], 2, True, False)
                self.notify(list[middle:], 2, False, False)
                self.notify(list[middle:], 1, True, False)
            
            left = self.mergesort(list[:middle],value)
            right = self.mergesort(list[middle:],value)
            
            return self.merge(left, right, value)
            
    def lenghtify(self, note, length): # convert length values to their lilypond reresentation
        if length == 1: 
            return note + "8 "
        elif length == 2: 
            return note + "4 "
        elif length == 3: 
            return note + "4. "
        elif length == 4: 
            return note + "2 "
        elif length == 5: 
            return note + "2 ~ " + note + "8 "        
        elif length == 6: 
            return note + "2. " 
        elif length == 7: 
            return note + "2 ~ " + note + "4. " 
        elif length == 8: 
            return note + "1 " 
        elif length == 9: 
            return note + "1 ~ " + note + "8 "
        elif length == 10: 
            return note + "1 ~ " + note + "4 "
        elif length == 11: 
            return note + "1 ~ " + note + "4. " 
        elif length == 12: 
            return note + "1 ~ " + note + "2 " 
        elif length == 13: 
            return note + "1 ~ " + note + "2 ~ " + note + "8 "
        elif length == 14: 
            return note + "1 ~ " + note + "2. "

    def pitchify(self, pitch): # convert pitch values to their lilypond representation
        if pitch == 0:
            return "r"
        elif pitch == 1:
            return "c,,"
        elif pitch == 2:
            return "cis,,"
        elif pitch == 3:
            return "d,,"
        elif pitch == 4:
            return "dis,,"
        elif pitch == 5:
            return "e,,"
        elif pitch == 6:
            return "f,," 
        elif pitch == 7:
            return "fis,,"
        elif pitch == 8:
            return "g,,"
        elif pitch == 9:
            return "gis,,"
        elif pitch == 10:
            return "a,,"
        elif pitch == 11:
            return "ais,,"
        elif pitch == 12:
            return "b,,"
        elif pitch == 13:
            return "c,"
        elif pitch == 14:
            return "cis,"
        elif pitch == 15:
            return "d,"
        elif pitch == 16:
            return "dis,"
        elif pitch == 17:
            return "e,"
        elif pitch == 18:
            return "f," 
        elif pitch == 19:
            return "fis,"
        elif pitch == 20:
            return "g,"
        elif pitch == 21:
            return "gis,"
        elif pitch == 22:
            return "a,"
        elif pitch == 23:
            return "ais,"
        elif pitch == 24:
            return "b,"
        elif pitch == 25:
            return "c"
        elif pitch == 26:
            return "cis"
        elif pitch == 27:
            return "d"
        elif pitch == 28:
            return "dis"
        elif pitch == 29:
            return "e"
        elif pitch == 30:
            return "f" 
        elif pitch == 31:
            return "fis"
        elif pitch == 32:
            return "g"
        elif pitch == 33:
            return "gis"
        elif pitch == 34:
            return "a"
        elif pitch == 35:
            return "ais"
        elif pitch == 36:
            return "b"
        elif pitch == 37:
            return "c'"
        elif pitch == 38:
            return "cis'"
        elif pitch == 39:
            return "d'"
        elif pitch == 40:
            return "dis'"
        elif pitch == 41:
            return "e'"
        elif pitch == 42:
            return "f'" 
        elif pitch == 43:
            return "fis'"
        elif pitch == 44:
            return "g'"
        elif pitch == 45:
            return "gis'"
        elif pitch == 46:
            return "a'"
        elif pitch == 47:
            return "ais'"
        elif pitch == 48:
            return "b'"
        elif pitch == 49:
            return "c''"
        elif pitch == 50:
            return "cis''"
        elif pitch == 51:
            return "d''"
        elif pitch == 52:
            return "dis''"
        elif pitch == 53:
            return "e''"
        elif pitch == 54:
            return "f''" 
        elif pitch == 55:
            return "fis''"
        elif pitch == 56:
            return "g''"
        elif pitch == 57:
            return "gis''"
        elif pitch == 58:
            return "a''"
        elif pitch == 59:
            return "ais''"
        elif pitch == 60:
            return "b''"
        elif pitch == 61:
            return "c'''"
    
    def notify(self, notes, voiceno, rest, merge): #Here the whole conversion thing is done. 
        if voiceno == 1:
            takt = self.resttakt_eins
        #    voice = "\\override NoteHead #\'color = #red \\override Stem #\'color = #red \\override Accidental #\'color = #red \n"
        if voiceno == 2:
            takt = self.resttakt_zwei
        #    voice = "\\override NoteHead #\'color = #green \\override Stem #\'color = #green \\override Accidental #\'color = #green \n"
        # this part was originally added to emphasize the merged notes, but i decided to leave that out because it's not necessary for playing
        # and is only meaningfu to specialists, anyway.
        # 
        #if merge == True:
        #    voice = "\\override NoteHead #\'color = #green \\override Stem #\'color = #green \\override Accidental #\'color = #green \n"
        #else:
        #    voice = "\\override NoteHead #\'color = #black \\override Stem #\'color = #black \\override Accidental #\'color = #black \n"
 
        voice = ""
        
        if rest == True:
            #voice = voice + "\\override Staff.Rest #\'color = #red \n"
            for note in notes: 
                if note[1] > 8:
                    restnote = note[1]     
                    while(restnote > 8):    
                        voice = voice + self.lenghtify("r", takt) + "~\n"     
                        restnote = restnote - takt
                        takt = 8
                    if restnote > takt:
                        voice = voice + self.lenghtify("r", takt) + "~\n" + self.lenghtify("r", restnote - takt) 
                        takt = 8 - (restnote - takt)
                    else:
                        voice = voice + self.lenghtify("r", restnote)
                        takt = takt - restnote
                elif takt < note[1]:
                    voice = voice + self.lenghtify("r", takt) + "~\n" + self.lenghtify("r", note[1] - takt)       
                    takt = 8 - (note[1] - takt)
                else:
                    voice = voice + self.lenghtify("r", note[1])
                    takt = takt - note[1]
                
                if takt == 0:
                    voice = voice + "\n" 
                    takt = 8 
  
        if rest == False:
            #voice = voice + "\\override Staff.Rest #\'color = #black \n"
            for note in notes:
                if note[1] > 8:
                    restnote = note[1]     
                    while(restnote > 8):    
                        voice = voice + self.lenghtify(self.pitchify(note[0]), takt) + "~\n"     
                        restnote = restnote - takt
                        takt = 8
                    if restnote > takt: 
                        voice = voice + self.lenghtify(self.pitchify(note[0]), takt) + "~\n" + self.lenghtify(self.pitchify(note[0]), restnote - takt)      
                        takt = 8 - (restnote - takt)
                    else: 
                        voice = voice + self.lenghtify(self.pitchify(note[0]), restnote)       
                        takt = takt - restnote
                elif takt < note[1]:
                    voice = voice + self.lenghtify(self.pitchify(note[0]), takt) + "~\n" + self.lenghtify(self.pitchify(note[0]), note[1] - takt)       
                    takt = 8 - (note[1] - takt)
                else:
                    voice = voice + self.lenghtify(self.pitchify(note[0]), note[1])
                    takt = takt - note[1]
                if takt == 0:
                    voice = voice + "\n" 
                    takt = 8 
        
            

        if voiceno == 1:
            self.resttakt_eins = takt
            self.voiceone = self.voiceone + voice 
        if voiceno == 2:
            self.resttakt_zwei = takt
            self.voicetwo = self.voicetwo + voice  


if __name__ == "__main__":
   
    american_in_paris_rip = [(56,9),
                             (58,1),(56,1),(49,1),(52,1),(51,1),(49,1),(46,1),
                             (44,14),(0,2),
                             (56,9),(58,1),(56,1),(49,1),(52,1),(51,1),(49,1),(46,1),
                             (49,14),(0,2), 
                             (56,1),(54,1),(49,1),(46,1),(45,1),(56,2),(54,1),
                             (53,1),(49,1),(45,1),(44,1),(43,1),(52,1),(42,1),(51,1),
                             (49,8)
                            ] 
    
    mySorter = sorter(american_in_paris_rip)
 
    mySorter.voiceone = mySorter.voiceone + "}"
    mySorter.voicetwo = mySorter.voicetwo + "}"

    mySorter.voiceone.replace("{", "{{")
    mySorter.voicetwo.replace("{", "{{")
    mySorter.voiceone.replace("}", "}}")
    mySorter.voicetwo.replace("}", "}}")
    
    # create folder for lilypond source files
    if not os.path.exists(foldername + "ly"):
        os.makedirs(foldername + "ly")

    if not os.path.exists(foldername + "pdf"):
        os.makedirs(foldername + "pdf")

    #print things to files
    v1sheet = open(foldername + 'ly/n_reppel_-_cleaning_up_an_american_in_paris_VOICE_A.ly', 'w')
    v2sheet = open(foldername + 'ly/n_reppel_-_cleaning_up_an_american_in_paris_VOICE_B.ly', 'w')
    scoresheet = open(foldername + 'ly/n_reppel_-_cleaning_up_an_american_in_paris_SCORE.ly', 'w')
    v1sheet.write(voice_one_file.format(mySorter.voiceone))
    v2sheet.write(voice_two_file.format(mySorter.voicetwo))
    scoresheet.write(score_file.format(mySorter.voiceone, mySorter.voicetwo))
    v1sheet.close()
    v2sheet.close()
    scoresheet.close()
    os.system("lilypond -V --output=" + foldername + "/pdf " + foldername + "ly/n_reppel_-_cleaning_up_an_american_in_paris_VOICE_A.ly")
    os.system("lilypond -V --output=" + foldername + "/pdf " + foldername + "ly/n_reppel_-_cleaning_up_an_american_in_paris_VOICE_B.ly")
    os.system("lilypond -V --output=" + foldername + "/pdf " + foldername + "ly/n_reppel_-_cleaning_up_an_american_in_paris_SCORE.ly")
    print("Cleaned up!")
