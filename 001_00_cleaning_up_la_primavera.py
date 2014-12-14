 # Cleaning up La Primavera 
 # La Primavera aufräumen
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
 # This is the generating source code for my piece "Cleaning Up La Primavera" 
 #
 # ====================
 # Some technical notes: (for musical notes, please read the introduction for the piece) 
 # ====================
 #
 # In this case, Notes are represented by a tuple, with the first value representing the pitch 
 # and the second value representing the length. 
 # The pitch value is (in this case) an integer, where 1 is "c,," going upwards in half tone steps, so that 2 is "cis,," etc. 
 # The length value is the number of sixteenth-notes so that 1 means the note is one sixteenth-note long, 4 means a 
 # quarter note etc. 
 # A rest ist represented by pitch value zero.
 # So, you can represent a melody as an array of tuples (as seen below).
 # 
 # The output of this little program is a lilypond file.
 #
import os

foldername = "001_cleaning_up_la_primavera/"

voice_one_file = """ 
\\version \"2.18.2\"

{0}

\\header {{
       title = \"La Primavera aufräumen\"
       subtitle = \"Cleaning up La Primavera \"
       subsubtitle= \"a very long violin solo"
       meter = \"ca. 160 bpm\"
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
  
class sorter():
    unsorted = []
    voiceone = "Stimmeeins = { \\key e \\major \\clef treble \\time 4/4 "
    mergedest = 1;
    restdest = 2;
    cutdest = 1;
    cutrestdest = 2;
    def __init__(self, notes):
        self.unsorted = notes
        self.resttakt_eins = 16
        self.notify(self.unsorted, 1, False, False) #the notify function writes the output notes in their lilypond representation
        self.bubblesort(self.bubblesort(self.unsorted, 1),0)#1st arg: list to be sorted 2nd arg: see below
 
    def bubblesort(self, notes, magicval): # a simple implementation of the bubblesort algorithm with note output
        n = len(notes)
        while(n > 1):
            for x in range(n-1):
                if notes[x][magicval] > notes[x+1][magicval]:
                    swap = notes[x]
                    notes[x] = notes[x+1]
                    notes[x+1] = swap
                    self.notify(notes, 1, False, False)
            n = n - 1 
        return notes
   
    def lenghtify(self, note, length): # convert length values to their lilypond reresentation
        if length == 1: 
            return note + "16 "
        elif length == 2: 
            return note + "8 "
        elif length == 3: 
            return note + "8. "
        elif length == 4: 
            return note + "4 "
        elif length == 5: 
            return note + "4 ~ " + note + "16 "        
        elif length == 6: 
            return note + "4. " 
        elif length == 7: 
            return note + "4 ~ " + note + "8. " 
        elif length == 8: 
            return note + "2 " 
        elif length == 9: 
            return note + "2 ~ " + note + "16 "
        elif length == 10: 
            return note + "2 ~ " + note + "8 "
        elif length == 11: 
            return note + "2 ~ " + note + "8. " 
        elif length == 12: 
            return note + "2. "  
       

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
    
        voice = ""
        
        if rest == True:
            for note in notes: 
                if note[1] > 16:
                    restnote = note[1]     
                    while(restnote > 16):    
                        voice = voice + self.lenghtify("r", takt) + "~\n"     
                        restnote = restnote - takt
                        takt = 16
                    if restnote > takt:
                        voice = voice + self.lenghtify("r", takt) + "~\n" + self.lenghtify("r", restnote - takt) 
                        takt = 16 - (restnote - takt)
                    else:
                        voice = voice + self.lenghtify("r", restnote)
                        takt = takt - restnote
                elif takt < note[1]:
                    voice = voice + self.lenghtify("r", takt) + "~\n" + self.lenghtify("r", note[1] - takt)       
                    takt = 16 - (note[1] - takt)
                else:
                    voice = voice + self.lenghtify("r", note[1])
                    takt = takt - note[1]
                
                if takt == 0:
                    voice = voice + "\n" 
                    takt = 16 
  
        if rest == False:
            for note in notes:
                if note[1] > 16:
                    restnote = note[1]     
                    while(restnote > 16):    
                        voice = voice + self.lenghtify(self.pitchify(note[0]), takt) + "~\n"     
                        restnote = restnote - takt
                        takt = 16
                    if restnote > takt: 
                        voice = voice + self.lenghtify(self.pitchify(note[0]), takt) + "~\n" + self.lenghtify(self.pitchify(note[0]), restnote - takt)      
                        takt = 6 - (restnote - takt)
                    else: 
                        voice = voice + self.lenghtify(self.pitchify(note[0]), restnote)       
                        takt = takt - restnote
                elif takt < note[1]:
                    voice = voice + self.lenghtify(self.pitchify(note[0]), takt) + "~\n" + self.lenghtify(self.pitchify(note[0]), note[1] - takt)       
                    takt = 16 - (note[1] - takt)
                else:
                    voice = voice + self.lenghtify(self.pitchify(note[0]), note[1])
                    takt = takt - note[1]
                if takt == 0:
                    voice = voice + "\n" 
                    takt = 16 
        
            

        if voiceno == 1:
            self.resttakt_eins = takt
            self.voiceone = self.voiceone + voice + " \\fermata "
       


if __name__ == "__main__":
   
    la_primavera_rip = [(53,2),(57,2),(57,2),(57,2),(55,1),(53,1),(60,6),(60,1),
                        (58,1),(57,2),(57,2),(57,2),(55,1),(53,1),(60,6),(60,1),(58,1),
                        (57,2),(58,1),(60,1),(58,2),(57,2),(55,2),(52,2),(48,2)
                        ] 
    
    mySorter = sorter(la_primavera_rip)
 
    mySorter.voiceone = mySorter.voiceone + "}"

    mySorter.voiceone.replace("{", "{{")
    mySorter.voiceone.replace("}", "}}")
    
    # create folder for lilypond source files
    if not os.path.exists(foldername + "ly"):
        os.makedirs(foldername + "ly")

    if not os.path.exists(foldername + "pdf"):
        os.makedirs(foldername + "pdf")

    #print things to files
    v1sheet = open(foldername + 'ly/n_reppel_-_cleaning_up_la_primavera.ly', 'w')

    v1sheet.write(voice_one_file.format(mySorter.voiceone))
    v1sheet.close()
  
    os.system("lilypond -V --output=" + foldername + "/pdf " + foldername + "ly/n_reppel_-_cleaning_up_la_primavera.ly")

    print("Cleaned up!")
