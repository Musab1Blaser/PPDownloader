from tkinter import *
from tkinter import font, messagebox

import requests
import os
import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup
header={'User-Agent': 'Mozilla/5.0'}

#Project initialisation
root=Tk()
root.title("Past Paper Downloader")

hei=600
wid=625
widhei=str(wid)+"x"+str(hei)
root.geometry(widhei)
currLevel=-1
LevelHeader=["O Levels","AS/A Levels", "IGCSE"]

def buildLevelFrame():    #Creates a frame containing the 3 buttons for the 3 different levels
    global LevelSelection
    LevelSelection=Frame(root)
    OLevelButton=Button(LevelSelection, text="O Levels", bg="#cc0000", fg="#ffffff", activebackground="#aa0000", activeforeground="#ffffff", height=3, width= 10, font=font.Font(family="Sans-serif",size=15), command=lambda: levelToSub(0))
    ALevelButton=Button(LevelSelection, text="AS/A Levels", bg="#cc0000", fg="#ffffff", activebackground="#aa0000", activeforeground="#ffffff", height=3, width= 10, font=font.Font(family="Sans-serif",size=15), command=lambda: levelToSub(1))
    IGCSEButton=Button(LevelSelection, text="IGCSE", bg="#cc0000", fg="#ffffff", activebackground="#aa0000", activeforeground="#ffffff", height=3, width= 10, font=font.Font(family="Sans-serif",size=15), command=lambda: levelToSub(2))
    OLevelButton.grid(row=0, column=0, padx=40, pady=100)
    ALevelButton.grid(row=0, column=1, padx=55, pady=100)
    IGCSEButton.grid(row=0, column=2, padx=50, pady=5)

def loadLevelFrame():
    global LevelSelection
    LevelSelection.pack(fill=BOTH, expand=1)  

def unloadLevelFrame():
    global LevelSelection
    LevelSelection.pack_forget()

def levelToSub(lev):
    unloadLevelFrame()    
    loadSubFrame(lev)

def loadSubFrame(lev):
    global SubjectSelection, SubjectControl, LevelHeader,currLevel, SubjectFrames
    SubjectSelection.pack(fill=BOTH, expand=1)
    SubjectFrames[lev].pack()
    Label(SubjectControl, text=LevelHeader[lev], font=font.Font(family="Sans-serif",size=20), width=13).grid(row=0,column=1, sticky="W")
    currLevel=lev

def unloadSubFrame(lev):
    global SubjectSelection, SubjectFrames
    SubjectSelection.pack_forget()
    SubjectFrames[lev].pack_forget()

def subToLoad(lev):
    unloadSubFrame(lev)
    loadLevelFrame()

def updateSearch(ent):
    searchItem=ent.get()
    global SubjectNames,SubjectButtons
    temp=0
    for sub in SubjectNames[currLevel]:
        if (searchItem.lower() in sub.lower()):
            SubjectButtons[currLevel][temp].grid(row=temp+1,column=0,pady=1, sticky="W")
        else:
            SubjectButtons[currLevel][temp].grid_forget()
        temp+=1

def buildSubjectFrame(): #each page consists of the control bar (with header + search and back button) and the main canvas and scrollbar (stored as lists as different canvases for different subject list)
    global SubjectSelection, currLevel,SubjectControl, SubjectNames, LevelHeader, SubjectFrames, SubjectButtons
    SubjectButtons=[]
    SubjectNames=[]
    subjectURLs=["https://papers.gceguide.com/O%20Levels/","https://papers.gceguide.com/A%20Levels/","https://papers.gceguide.com/Cambridge%20IGCSE/"]

    SubjectSelection=Frame(root)
    SubjectControl=Frame(SubjectSelection)
    SubjectControl.pack()

    SubjectBackButton=Button(SubjectControl, text="Return to Level Selection", bg="#0000cc", fg="#ffffff", activebackground="#0000aa", activeforeground="#ffffff", height=2, width= 22, font=font.Font(family="Sans-serif",size=15), command=lambda: subToLoad(currLevel))
    SubjectBackButton.grid(row=1, column=0, rowspan=2, pady=4)
    
    SubjectSearch=Label(SubjectControl,text="Search:", font=font.Font(family="Sans-serif",size=11))
    SubjectSearch.grid(row=1, column=2)
    SearchEntry=StringVar()
    SearchEntry.trace("w", lambda name, index,mode, SearchEntry=SearchEntry: updateSearch(SearchEntry))
    subEntry=Entry(SubjectControl, textvariable=SearchEntry)
    subEntry.grid(row=2, column=2)

    SubjectCanvas=Canvas(SubjectSelection)
    SubjectScrollbar=Scrollbar(SubjectSelection, orient=VERTICAL, command=SubjectCanvas.yview)
    SubjectCanvas.configure(yscrollcommand=SubjectScrollbar.set)
    SubjectCanvas.bind('<Configure>', lambda e: SubjectCanvas.configure(scrollregion=SubjectCanvas.bbox("all")))
    def _on_mouse_wheel(event):
        SubjectCanvas.yview_scroll(-1 * int((event.delta / 120)), "units")
    SubjectCanvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    AllSubjectFrame=Frame(SubjectCanvas)
    SubjectCanvas.create_window((0,0), window=AllSubjectFrame, anchor="nw")
    SubjectCanvas.pack(side=LEFT, fill=BOTH, expand=True)
    SubjectScrollbar.pack(side=RIGHT, fill=Y, expand=True, anchor="e")

    SubjectFrames=[]
    for subjectURL in subjectURLs:
        SubjectFrames.append(Frame(AllSubjectFrame))
        SubjectButtons.append([])
        loadSubjects(subjectURL)

def loadSubjects(url):
    global header
    req = urllib.request.Request(url, headers=header)
    html=urllib.request.urlopen(req).read() #.read gives the contents of the file
    soap=BeautifulSoup(html,'html.parser')
    soup=soap.find("ul", {"id": "paperslist"})
    tags=soup('a')
    global SubjectButtons, SubjectNames, SubjectFrames
    SubjectNames.append([tag.get('href') for tag in tags])
    temp=len(SubjectButtons)-1
    r=1
    for sub in SubjectNames[-1]:
        SubjectButtons[temp].append(Button(SubjectFrames[-1], text=sub, height=2, width=len(sub)+3, command=lambda sub=sub:subToYear(sub, urllib.parse.urljoin(url,sub.replace(" ","%20"))+"/"), bg="#cc0000", fg="#ffffff", activebackground="#aa0000", activeforeground="#ffffff"))
        SubjectButtons[temp][r-1].grid(row=r,column=0, pady=1, sticky="W")
        r+=1

def subToYear(sub, url):
    global currLevel
    unloadSubFrame(currLevel)
    loadYearFrame(sub,url)

def loadYearFrame(sub,url):
    global currURL, currSub
    global YearSelection
    YearSelection.pack()
    loadYearControl(sub)
    loadYearList(url)
    currURL=url
    currSub=sub

def yearToSub(currLevel):
    loadSubFrame(currLevel)
    unloadYearFrame()

def unloadYearFrame():
    YearSelection.pack_forget()
    unloadYearControl()
    unloadYearList()

def buildYearFrame():
    global YearSelection, YearControl, YearList, FolderSettings, CompEnt, selectedYears
    YearSelection=Frame(root)
    YearControl=Frame(YearSelection)
    YearList=Frame(YearSelection)
    FolderSettings=Frame(YearSelection)
    YearControl.pack()
    YearList.pack(pady=5)
    FolderSettings.pack()
    FoldName=Frame(FolderSettings)
    SubFold=Frame(FolderSettings)
    SortFiles=Frame(FolderSettings)
    FoldName.grid(row=0, column=0, padx=2)
    SubFold.grid(row=0, column=1,padx=4)
    SortFiles.grid(row=0, column=2,padx=2)

    #Folder Settings
    #Session Folder Names
    Label(FoldName, text="Session Folder Names").pack()
    abb_full=IntVar()
    abb_full.set(0)
    abb=Radiobutton(FoldName,text="MJ/ON/FM", variable=abb_full, value=0)
    full=Radiobutton(FoldName,text="May/Nov/March", variable=abb_full, value=1)
    abb.pack(anchor="w")
    full.pack(anchor="w")
    
    #Subfolders Selection
    yearFolder=IntVar()
    compFolder=IntVar()
    Label(SubFold, text="Subfolders").pack()
    yearFoldButton=Checkbutton(SubFold, text="Years", variable=yearFolder)
    compFoldButton=Checkbutton(SubFold, text="Components", variable=compFolder)
    yearFoldButton.pack(anchor="w")
    compFoldButton.pack(anchor="w")

    #File Sorting Selection
    Label(SortFiles, text="Sort Files").pack()
    sortSelection=IntVar()
    sortSelection.set(0)
    mqmq=Radiobutton(SortFiles,text="Sort each QP after its MS", variable=sortSelection, value=0)
    mmqq=Radiobutton(SortFiles,text="Sort all QP together and MS together", variable=sortSelection, value=1)
    mqmq.pack(anchor="w")
    mmqq.pack(anchor="w")

    #Download Button
    DownloadButton=Button(FolderSettings, text="Download", bg="#f35f1b", fg="#ffffff", activebackground="#f4a923", activeforeground="#ffffff", height=2, width= 11, font=font.Font(family="Sans-serif",size=17), command=lambda: downloadFiles(currURL, selectedYears,(CompEnt.get()).replace(" ","").split(","),abb_full.get(),yearFolder.get(),compFolder.get(),sortSelection.get()))
    DownloadButton.grid(row=0, column=3, padx=4)

def loadYearControl(sub):
    global YearControl, currLevel, CompEnt #adds header + back button + component entry + select all button
    Label(YearControl, text=LevelHeader[currLevel]+" -> "+sub, font=font.Font(family="Sans-serif",size=8), width=35).grid(row=0,column=1)
    YearBackButton=Button(YearControl, text="Return to Subject Selection", bg="#0000cc", fg="#ffffff", activebackground="#0000aa", activeforeground="#ffffff", height=2, width= 20, font=font.Font(family="Sans-serif",size=10), command=lambda: yearToSub(currLevel))
    YearBackButton.grid(row=1, column=0, rowspan=2, pady=4)
    ComponentLabel=Label(YearControl,text="Enter component number (comma separated e.g. 2,3,5)")
    ComponentLabel.grid(row=1, column=1)
    CompEnt=Entry(YearControl)
    CompEnt.grid(row=2,column=1)
    SelectAllButton=Button(YearControl, text="Select All", bg="#00cc00", fg="#ffffff", activebackground="#00aa00", activeforeground="#ffffff", height=2, width= 14, font=font.Font(family="Sans-serif",size=10), command=selectAll)
    SelectAllButton.grid(row=1, column=2, rowspan=2, pady=4)

def selectAll(): #selects all years
    global selectedYears
    found=1
    for i in selectedYears:
        found=i.get()
        if found==0:
            break
    if found==0:
        for i in selectedYears:
            i.set(1)
    else:
        for i in selectedYears:
            i.set(0)

def loadYears(url):
    global header, yearList, YearBoxes, selectedYears, YearList
    req=urllib.request.Request(url, headers=header)
    html=urllib.request.urlopen(req).read()
    soap=BeautifulSoup(html,'html.parser')
    soup=soap.find("ul", {"id":"paperslist"})
    tags=soup('a')
    yearList=[tag.get("href") for tag in tags]
    selectedYears=[]
    YearBoxes=[]
    for year in yearList: #yearBoxes stores the checkboxes and selectedYears stores the variable carrying state of each year
        tempVar=IntVar()
        tempVar.set(0)
        selectedYears.append(tempVar)
        YearBoxes.append(Checkbutton(YearList, text=year, variable=selectedYears[-1]))

def loadYearList(url):
    global YearBoxes
    loadYears(url)
    for i in range(len(YearBoxes)):
        YearBoxes[i].grid(row=int(i/2), column=i%2)
        
def unloadYearList():
    global YearList
    for widget in YearList.winfo_children():
        widget.destroy()

def unloadYearControl():
    global YearControl
    for widget in YearControl.winfo_children():
        widget.destroy()

def downloadFiles(url, yearVarList, compList, fname, yFold, cFold, sortSelection):
    global yearList, yearFiles

    noYears=True
    for i in yearVarList:
        if i.get()==1:
            noYears=False
    if ((len(compList)==1) and len(compList[0])==0) or noYears:
        messagebox.showwarning("Error","No Components and/or Years selected. Please reselect and Try again")
    else:
        years=[]
        yearFiles=[]
        for i in range(len(yearList)):
            if yearVarList[i].get()>=1:
                years.append(yearList[i])
                loadFilesYear(url,yearList[i], compList)
        totalFiles=0
        # print(yearFiles)
        # print("Years: ",years)
        for y in yearFiles:
            totalFiles+=len(y)
        
        i=0
        for year in years:
            for filename in yearFiles[i]:
                file_url=currURL+year.replace(" ","%20")+"/"+filename
                downloadFile(file_url, fname, yFold, cFold, year, filename, sortSelection)
            i+=1
        unloadYearFrame()
        loadSubFrame(currLevel)

def downloadFile(file_url, fname, yFold, cFold, year, filename, sortSelection):
    # print(file_url)
    cwd = os.getcwd()
    subFolder = os.path.join(cwd,currSub)
    if not os.path.exists(subFolder):
        os.mkdir(subFolder)

    path=subFolder
    if yFold==1 or not(year.isnumeric()):
        path=os.path.join(subFolder,year)
        if not os.path.exists(path):
            os.mkdir(path)

    opts=[["-MJ","-ON","-FM"],["-May","-Nov","-March"]]
    r=fname
    c=0
    if filename[5]=="m":
        c=2
    elif filename[5]=="w":
        c=1
    elif filename[5]=="s":
        c=0
    
    if year.isnumeric():
        foldName=year[-2:]+opts[r][c]        
        path=os.path.join(path,foldName)
        if not os.path.exists(path):
            os.mkdir(path)

    temp=filename.split("_")
    if cFold==1:
        try:
            if len(temp)==4 and year!="Other Resources":
                comp="P"+str(int((temp[3].split("."))[0]))[0]
                path=os.path.join(path,comp)
                if not os.path.exists(path):
                    os.mkdir(path)
        except:
            pass

    if sortSelection==0 and len(temp)==4:
        if temp[2]=="qp" or temp[2]=="ms":
            tem=temp[3].split(".")
            filename=temp[0]+"_"+temp[1]+"_"+"p"+tem[0]+"_"+temp[2]+"."+tem[1]

    path=os.path.join(path,filename)
    resp=requests.get(file_url)
    f=open(path, "wb")
    for chunk in resp.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
    # with open(path, "wb") as f:
    #     try:
    #         for chunk in r.iter_content(chunk_size=1024):
    #             if chunk:
    #                 f.write(chunk)
    #     except:
    #        return

        

def loadFilesYear(url, year, compList):
    global yearFiles
    yearFiles.append([])
    tempURL=urllib.parse.urljoin(url,year.replace(" ","%20"))+"/"
    req = urllib.request.Request(tempURL, headers=header)
    html=urllib.request.urlopen(req).read() #.read gives the contents of the file
    soap=BeautifulSoup(html,'html.parser')
    soup=soap.find("ul", {"id": "paperslist"})
    tags=soup('a')
    for tag in tags:
        yearFile=tag.get("href")
        temp=yearFile.split("_")
        yearFiles[-1].append(yearFile)
        if len(temp)>3 and year!="Other Resources":
            try:
                if not(str(int(temp[3].split(".")[0]))[0] in compList):
                    yearFiles[-1].pop()
            except:
                continue
    

buildLevelFrame()
buildSubjectFrame()
buildYearFrame()
loadLevelFrame()

root.mainloop()