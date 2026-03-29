
# CleanData Method 
def CleanData(rawdata,cp):
    """
    Rawdata and cp only acceptable in list type
    require no modules 
    """    
    readings=[]
    cp_count=0                                    

    for index,data in enumerate(rawdata,start=1):
        row={
            "station":"",
            "type":"",
            "value":""
        }
        if index==1:                                  # FOR FIRST READING 
            row["station"]="BM"
            row["type"]="BS"
            row["value"]=float(data)
            
        elif index in cp:                              # FOR CHANGE POINTS 
            cp_count += 1
            row["station"]="CP"+str(cp_count)  
            row["type"]="FS"
            row["value"]=float(data)
            
        elif index==len(rawdata):                      # FOR LAST READINGS
            row["station"]="P"+str(index-cp_count)
            row["type"]="FS"
            row["value"]=float(data)
            
        else :
            for cp_point in cp :
                status=False
                if index-cp_point==1:                   # FOR BS POINTS AFTER CHANGE POINTS
                    row["station"]="CP"+str(cp_count)
                    row["type"]="BS"
                    row["value"]=float(data)
                    status=True
                    break
                    
            if status==False:                            # FOR IS READINGS   
                row["station"]="P"+str(index-cp_count)
                row["type"]="IS"
                row["value"]=float(data)
        readings.append(row)    
    return readings  



# HI Level Method
def HiMethod(readings,bm_rl):           # READINGS AS LIST AND BM_RL IS BENCHMARK OF 1ST READING 
    import pandas as pd
    results=[]                                          # STORE ALL OUTPUTS
    current_rl=bm_rl                                    # 1ST READING BENCHMARK 
    i=0

    while i < len(readings):                            # LOOP FOR ALL READNGS AND SKIPPING BS OF CP 
        r=readings[i]
        rstation=r["station"]
        rtype=r["type"]
        rvalue=r["value"]


        row={                                           # ROW FOR TABLE FORMAT 
            "STATION":rstation,
            "BS":"",
            "IS":"",
            "FS":"",
            "HI":"",
            "RL":"",
            "Remarks":""
        }

        if rstation=="BM" :                               # FOR BENCHMARK OR FIRST READING 
            current_hi=current_rl+rvalue
            row["BS"]=rvalue
            row["HI"]=round(current_hi,3)
            row["RL"]=current_rl
        elif rtype=="IS":                               # FOR IS POINT 
            current_rl=current_hi-rvalue
            row["IS"]=rvalue
            row["RL"]=round(current_rl,3)
        elif rtype=="FS" and rstation.startswith("CP"):     # FOR CHANGE POINT 
            if i+1 < len(readings) and readings[i+1]["type"]=="BS" and readings[i+1]["station"].startswith("CP") :                             # CHECKS THE NEXT READING 
                fs_value=rvalue
                bs_value=readings[i+1]["value"]
                current_rl=current_hi - fs_value
                current_hi=current_rl+bs_value
                row["BS"]=round(bs_value,3)
                row["FS"]=round(fs_value,3)
                row["HI"]=round(current_hi,3)
                row["RL"]=round(current_rl,3)
                row["Remarks"]=rstation
                i += 1                               # SKIP NEXT 1 READING 
        elif rtype=="FS" :                                       # FOR LAST FS   
            current_rl = current_hi - rvalue 
            row["FS"]=rvalue
            row["RL"]=round(current_rl,3)
            row["Remarks"]="LastFS"
        if i+1 ==len(readings):
            last_rl=current_rl    
        i += 1                                        # CONTINUES THE LOOP
        results.append(row)                           # APPEND EVERY CALCULATED ROW 
    return pd.DataFrame(results),last_rl                      # RETURNS THE RESULTS IN PANDAS DATAFRAME 
  


# RiseFall Method
def RiseFallMethod(readings,bm_rl):
    """
    readings parameter -- list 
    bm_rl -- float (RL of first point )
    require pandas module 

    """
    import pandas as pd
    results=[]
    current_rl=bm_rl                       # RL OF BENCHMARK 
    prev_type=None
    prev_reading=None
    cp_count=1

    i=0
    while i < len(readings):
        r=readings[i]
        rstation=r["station"]
        rtype=r["type"]
        rvalue=r["value"]

        row={                                     # ROW FOR OUTPUT TABLE FOR EACH READINGS
            "STATION":rstation,
            "BS":"",
            "IS":"",
            "FS":"",
            "RISE":"",
            "FALL":"",
            "RL":"",
            "REMARKS":""
        }
        if i==0:                            # 1ST READING AS BENCHMARK
            row["BS"]=rvalue
            row["RL"]=round(current_rl,3)
            row["REMARKS"]=rstation
            prev_type=rtype
            prev_reading=rvalue
            results.append(row)
            i +=1
            continue
        if (                                  # FOR CHANGE POINT ( FS AND BS IN SAME ROW )
            i +1 < len(readings)
            and readings[i+1]["type"]=="BS"
            and readings[i+1]["station"].startswith("CP")
            and rstation.startswith("CP")
            ):
            fs_value=rvalue
            bs_value=readings[i+1]["value"]

            # RISE/FALL BASED ON DIFF
            diff=prev_reading-fs_value
            if diff > 0 :
                row["RISE"]=round(diff,3)
                current_rl += diff
            elif diff < 0 :
                row["FALL"]=round(abs(diff),3)
                current_rl -= abs(diff)
            row["BS"]=round(bs_value,3) 
            row["FS"]=round(fs_value,3)
            row["RL"]=round(current_rl,3)
            row["REMARKS"]="CP"+str(cp_count)
            
            prev_reading=bs_value
            cp_count += 1                         # FOR CHANGE POINT COUNT 
            i += 2                                # SKIPS THE NEXT 1 READING 
            results.append(row)
            continue 

        # ------- FOR NORMAL POINTS ------
        diff=prev_reading - rvalue 
        if diff > 0: 
            row["RISE"]=round(diff,3)
            current_rl += diff
        elif diff < 0 : 
            row["FALL"]=round(abs(diff),3)
            current_rl -= abs(diff)
        if rtype=="BS":
            row["BS"]=rvalue 
        elif rtype=="IS":
            row["IS"]=rvalue
        elif rtype=="FS":
            row["FS"]=rvalue
            row["REMARKS"]="LAST FS"

        row["RL"]=round(current_rl,3)
        prev_reading=rvalue
        if i+1==len(readings):
            last_rl=current_rl
        i += 1
        results.append(row)
    return pd.DataFrame(results),last_rl            # RETURN AD DATAFRAME FOR FURTHER TASKS  