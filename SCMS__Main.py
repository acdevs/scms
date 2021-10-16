#*****************Sports Club Management System*******************

#INFO: Connectivity using Xampp -> Mariadb
#modules needed:  mysql.connector,datetime,time

import mysql.connector, datetime, time
try:
    db=mysql.connector.connect(host='localhost',user='root',password='',database='scms')
    if db.is_connected():
        print('Welcome To Sports Club Management System Service.\n')
    else:
        print('Oops! Database Connection Failed.')
        exit()
except:
    print('Internal Server Error Occurred !')
    time.sleep(1.5)
    exit()

class Validate:
    def date(strdate):
        year,month,day=[int(i) for i in strdate.split('-')]
        months=([1,31],[2,28],[3,31],[4,30],[5,31],[6,30],[7,31],[8,31],[9,30],[10,31],[11,30],[12,31])
        curYear=datetime.date.today().year
        if 1990<=year<=curYear and 1<=month<=12:
            if month==2 and (not year%4 and not year%400 or not year%4 and year%100): #leapYear checking
                months[1][1]=29
            days31 = month in [i for i,j in months if j==31 ] and 1<=day<=31 #conditions stored in vars
            days30 = month in [i for i,j in months if j==30 ] and 1<=day<=30
            daysFeb = month==2 and 1<=day<=months[1][1]
            if days30 or days31 or daysFeb:
                return True
            else:
                return False
        else:
                return False
    
class MemberMenu:
    header=['SrNo','MemberCode','MemberName','DateOfJoining','Address',
            'PhoneNumber','Facility1','Facility2','Facility3','Children']

    def is_existing(fcode):                  #For Validation of facilityCode entry
        memCursor=db.cursor(buffered=True)
        sql=f'select facilityCode from facility where facilityCode={fcode}'
        memCursor.execute(sql)
        if memCursor.rowcount==1:
            return True
        else:
            return False
        
    def reg(): #registration
        print('New Registration')
        memCursor=db.cursor(buffered=True)
        code=int(input('Member Code: '))
        memCursor.execute(f'select memberCode from member where memberCode={code}')
        if memCursor.rowcount in (0,-1):
            name=input('Member Name: ')
            while True:
                doj=input('Date of joining[yyyy-mm-dd]: ')
                if Validate.date(doj):
                    break
                else:
                    print('>>> Invalid Date. Enter again...')
                    continue
            add=input('Address: ')
            pn=int(input('Phone Number: '))
            while True:
                fc1=int(input('Facility Code1: '))
                if MemberMenu.is_existing(fc1):
                    break
                else:
                    print('>>> This facilityCode is not existing in Facility!')
                    continue
            while True:
                fc2=int(input('Facility Code2: '))
                if MemberMenu.is_existing(fc2):
                    break
                else:
                    print('>>> This facilityCode is not existing in Facility!')
                    continue
            while True:
                fc3=int(input('Facility Code3: '))
                if MemberMenu.is_existing(fc3):
                    break
                else:
                    print('>>> This facilityCode is not existing in Facility!')
                    continue
            child=int(input('Number of Children: '))
            sql='insert into member values({},"{}","{}","{}",{},{},{},{},{})'.format(code,name,doj,add,pn,fc1,fc2,fc3,child)
            memCursor.execute(sql)
            db.commit()
            print('>>> Success! 1 record registered.\n')
        else:
            print('>>> Member Code is already existing!\n')
    def mod(): #modification
        memCursor=db.cursor(buffered=True)
        print('Modify A Record Using :-')
        code=int(input('Member Code    : '))
        memCursor.execute(f'select * from member where memberCode={code}')
        if memCursor.rowcount in (0,-1):
            print('>>> Member Code is not existing!\n')
        else:
            rec=memCursor.fetchone()
            print('Member Name    :',rec[1])
            print('Date of Joining:',rec[2])
            print('Address        :',rec[3])
            print('Phone Number   :',rec[4])
            print('Facility Code 1:',rec[5])
            print('Facility Code 2:',rec[6])
            print('Facility Code 3:',rec[7])
            print('Children       :',rec[8])
            print('\nNew Entries: ')
              # New Entries
            name=input('Member Name: ')
            while True:
                doj=input('Date of joining[yyyy-mm-dd]: ')
                if Validate.date(doj):
                    break
                else:
                    print('>>> Invalid Date. Enter again...')
                    continue
            add=input('Address: ')
            pn=int(input('Phone Number: '))
            while True:
                fc1=int(input('Facility Code1: '))
                if MemberMenu.is_existing(fc1):
                    break
                else:
                    print('>>> This facilityCode is not existing in Facility!')
                    continue
            while True:
                fc2=int(input('Facility Code2: '))
                if MemberMenu.is_existing(fc2):
                    break
                else:
                    print('>>> This facilityCode is not existing in Facility!')
                    continue
            while True:
                fc3=int(input('Facility Code3: '))
                if MemberMenu.is_existing(fc3):
                    break
                else:
                    print('>>> This facilityCode is not existing in Facility!')
                    continue
            child=int(input('Number of Children: '))
            sql='update member set memberName="{}" , dateOfJoining="{}" , address="{}" ,\
            phoneNumber={} , facilityCode1={} ,  facilityCode2={} ,  facilityCode3={} , children={} \
            where memberCode={}'.format(name,doj,add,pn,fc1,fc2,fc3,child,code)
            memCursor.execute(sql)
            db.commit()
            print('>>> Success! 1 record modified.\n')
            
    def delt(): #deletion
        memCursor=db.cursor(buffered=True)
        print('Delete A Record Using :-')
        code=int(input('Member Code    : '))
        memCursor.execute(f'select * from member where memberCode={code}')
        if memCursor.rowcount in (0,-1):
            print('>>> Member Code is not existing!\n')
        else:
            rec=memCursor.fetchone()
            print('Member Name    :',rec[1])
            print('Date of Joining:',rec[2])
            print('Address        :',rec[3])
            print('Phone Number   :',rec[4])
            print('Facility Code 1:',rec[5])
            print('Facility Code 2:',rec[6])
            print('Facility Code 3:',rec[7])
            print('Children       :',rec[8])
            print()
            confirm=input('Do you want DELETE this information? [y/n]: ').lower()
            if confirm=='y':
                #Need to clear fee entries for that member first!!! [foreign key integrity]
                fee_sql=f'delete from fees where memberCode={code}'
                memCursor.execute(fee_sql)
                sql=f'delete from member where memberCode={code}'
                memCursor.execute(sql)
                db.commit()
                print('>>> Success! 1 record deleted.\n')
            else:
                print('>>> Deletion Aborted!\n')
                
                
    def det(): #details display
        memCursor=db.cursor(buffered=True)
        print('''Search Using [Make a number choice]:-
                1. Member Code
                2. Member Name
                3. Phone Number''')
        chosen=int(input())
        if chosen==1:
            code=int(input('Member Code    : '))
            memCursor.execute(f'select * from member where memberCode={code}')
            if memCursor.rowcount in (0,-1):
                print('>>> No information found!\n')
            else:
                rec=memCursor.fetchone()
                print('Member Name    :',rec[1])
                print('Date of Joining:',rec[2])
                print('Address        :',rec[3])
                print('Phone Number   :',rec[4])
                print('Facility Code 1:',rec[5])
                print('Facility Code 2:',rec[6])
                print('Facility Code 3:',rec[7])
                print('Children       :',rec[8])
                print('>>> Record Matched!\n')
        elif chosen==2:
            name=input('Member Name    : ')
            memCursor.execute(f'select * from member where memberName="{name}"')
            if memCursor.rowcount in (0,-1):
                print('>>> No information found!\n')
            else:
                rec=memCursor.fetchone()
                print('Member Code    :',rec[0])            #they are unique or not ?
                print('Date of Joining:',rec[2])
                print('Address        :',rec[3])
                print('Phone Number   :',rec[4])
                print('Facility Code 1:',rec[5])
                print('Facility Code 2:',rec[6])
                print('Facility Code 3:',rec[7])
                print('Children       :',rec[8])
                print('>>> Record Matched!\n')
        elif chosen==3:
            pn=int(input('Phone Number   : '))
            memCursor.execute(f'select * from member where phoneNumber={pn}')
            if memCursor.rowcount in (0,-1):
                print('>>> No information found!\n')
            else:
                rec=memCursor.fetchone()
                print('Member Code    :',rec[0])
                print('Member Name    :',rec[1])
                print('Date of Joining:',rec[2])
                print('Address        :',rec[3])
                print('Facility Code 1:',rec[5])
                print('Facility Code 2:',rec[6])
                print('Facility Code 3:',rec[7])
                print('Children       :',rec[8])
                print('>>> Record Matched!\n')


class FeeMenu:
    def is_existing(code):                #For Validation of entries
        feeCursor=db.cursor(buffered=True)
        sql=f'select memberCode from member where memberCode={code}'
        feeCursor.execute(sql)
        if feeCursor.rowcount==1:
            return True
        else:
            return False
        
    def entry(): #entry of fees
        print('New Fee Entry.')
        feeCursor=db.cursor(buffered=True)
        code=int(input('Member Code: '))
        if FeeMenu.is_existing(code):
            while True:
                    dos=input('Date of Submission[yyyy-mm-dd]: ')
                    if Validate.date(dos):
                        break
                    else:
                        print('>>> Invalid Date. Enter again...')
                        continue
            feeCursor.execute(f'select * from fees where memberCode={code} and dateOfSubmission="{dos}"')
            counts=feeCursor.rowcount
            if counts==1:
                print(f'>>> The fee entry for the member, paid fee on {dos}, is already existing!\n')
            else:
                amu=float(input('Amount: '))
                sql='insert into fees values({},"{}",{})'.format(code,dos,amu)
                feeCursor.execute(sql)
                db.commit()
                print('>>> Success! fee entry registered.\n')
        else:
            print(f'>>> The Member with Code: {code} does not exists in Members.\n')

    
    def det(): #fee details of a member
        feeCursor=db.cursor(buffered=True)
        print('Search Using:-')
        code=int(input('Member Code       : '))
        feeCursor.execute(f'select * from fees where memberCode={code}')
        counts=feeCursor.rowcount
        if counts in (0,-1):
            print('>>> No information found!\n')
        else:
            records=feeCursor.fetchall()
            print('Date of Submission:', ','.join([str(rec[1]).ljust(12) for rec in records]))  #displaying Horizonatlly
            print('Amount            :', ','.join([str(rec[2]).ljust(12) for rec in records]))  #So display problem 
            print(f'>>> {counts} Records Matched!\n')
                
class FacilityMenu:
    def new(): #new facility
        print('New facility.')
        facCursor=db.cursor(buffered=True)
        code=int(input('Facility Code: '))
        facCursor.execute(f'select facilityCode from facility where facilityCode={code}')
        if facCursor.rowcount in (0,-1):
            fac=input('Facility     : ')
            sql='insert into facility values({},"{}")'.format(code,fac)
            facCursor.execute(sql)
            db.commit()
            print('>>> Success! facility added.\n')
        else:
            print('>>> Facility Code is already existing!.\n')
        
    def det(): #facility details
        feeCursor=db.cursor(buffered=True)
        print('Facility Details:-')
        feeCursor.execute('select * from facility')
        counts=feeCursor.rowcount
        if counts in (0,-1):
            print('>>> No information found!\n')
        else:
            print('FacilityCode','Facility')
            print('------------','--------')
            records=feeCursor.fetchall()
            for rec in records:
                print(str(rec[0]).ljust(12),rec[1])
            print()
                               
class ReportMenu:
    def display(header,records,heading):
        hchr='-'
        centvalue=[]
        index=0
        records.insert(0,header)
        #determining center value for each column
        for i in range(len(header)):
                centvalue.append(0)
                for j in range(len(records)):
                        if centvalue[index]<len(str(records[j][i])):
                                centvalue[index]=len(str(records[j][i]))+1 #for clarity
                index+=1
        index=0
        borderlen=sum(centvalue)+len(header)+1
        print('Sports Club'.center(borderlen))
        print(heading.center(borderlen))
        date=datetime.datetime.now().strftime("%d/%m/%y") 
        print(f'Date:  {date} '.rjust(borderlen))
        print(hchr*borderlen)
        l=0
        for record in records:
                index=0
                for item in record:
                    if type(item) in (int,float):
                        print(f'|{str(item).center(centvalue[index])}',end='')
                    else:
                        print(f'|{str(item).ljust(centvalue[index])}',end='')
                    index+=1
                print('|')
                if l==0:
                   print(hchr*borderlen)
                l=1
        print(hchr*borderlen)

    def memberDetails(): #member details
        t1=time.process_time()#time start
        repCursor=db.cursor(buffered=True)
        fac={}
        fac_sql='select * from facility'
        repCursor.execute(fac_sql)   #facility fetched
        for f1,f2 in repCursor:
            fac.update({f1:f2.capitalize()})
        member_sql='select * from member' 
        repCursor.execute(member_sql)
        counts=repCursor.rowcount
        if counts in (0,-1):
            print('>>> No Details found!\n')
        else:
            heading='MEMBER LIST'
            fetched=repCursor.fetchall()
            records=[[i+1]+list(fetched[i]) for i in range(len(fetched))]
            for rec in records:
                for index in range(6,9):
                    if rec[index] in fac:
                        rec[index]=fac[rec[index]]
            ReportMenu.display(MemberMenu.header,records,heading) #so pretty
            t2=time.process_time()#time stops
            print(f'>>> {round(t2-t1,2)}s, {counts} Records Processed!\n')

            
    def activityDetails(): #activity details
        t1=time.process_time()#time start
        repCursor=db.cursor(buffered=True)
        header=['SrNo','Activity','MemberCode','MemberName']
        sql='select facility,memberCode,memberName from facility,member where\
        facilityCode in (facilityCode1,facilityCode2,facilityCode3) order by facility' 
        repCursor.execute(sql)
        counts=repCursor.rowcount
        if counts in (0,-1):
            print('>>> No Details found!\n')
        else:
            heading='ACTIVITYWISE MEMBER LIST'
            fetched=repCursor.fetchall()
            records=[[i+1]+list(fetched[i]) for i in range(len(fetched))]
            ReportMenu.display(header,records,heading) #so pretty
            t2=time.process_time()#time stops
            print(f'>>> {round(t2-t1,2)}s, {counts} Records Processed!\n')
            
    def dwFeeDetails(): #date wise fee details
        t1=time.process_time()#time start
        repCursor=db.cursor(buffered=True)
        header=['SrNo','Date','MemberCode','MemberName','Amount']
        sql='select dateOfSubmission,m.memberCode,memberName,Amount from fees f,member m where m.memberCode=f.memberCode \
        order by dateOfSubmission' 
        repCursor.execute(sql)
        counts=repCursor.rowcount
        if counts in (0,-1):
            print('>>> No Details found!\n')
        else:
            heading='DATEWISE FEE DETAILS'
            fetched=repCursor.fetchall()
            records=[[i+1]+list(fetched[i]) for i in range(len(fetched))]
            ReportMenu.display(header,records,heading) #so pretty
            t2=time.process_time()#time stops
            print(f'>>> {round(t2-t1,2)}s, {counts} Records Processed!\n')

            
    def odFeeDetails(): #over due fee details
        t1=time.process_time()#time start
        repCursor=db.cursor(buffered=True)
        header=['SrNo','MemberCode','MemberName','LastFeeSubmissionDate',] #date_add(max(dateOfSubmission),interval 6 month)
        sql='select m.memberCode,memberName,max(dateOfSubmission) from fees f,member m\
        where m.memberCode=f.memberCode group by m.memberCode having datediff(curdate(),max(dateOfSubmission))>180' 
        repCursor.execute(sql)
        counts=repCursor.rowcount
        if counts in (0,-1):
            print('>>> No Details found!\n')
        else:
            heading='OVERDUE FEE DETAILS'
            fetched=repCursor.fetchall()
            records=[[i+1]+list(fetched[i]) for i in range(len(fetched))]
            ReportMenu.display(header,records,heading) #so pretty
            t2=time.process_time()#time stops
            print(f'>>> {round(t2-t1,2)}s, {counts} Records Processed!\n')

            
    def memberCard(): #membership card
        t1=time.process_time()#time start
        repCursor=db.cursor(buffered=True)
        code=int(input('Member Code    : '))
        repCursor.execute(f'select * from member where memberCode={code}')
        if repCursor.rowcount in (0,-1):
            print('>>> No Member exists!\n')
        else:
            rec=repCursor.fetchone()
            fac={}
            fac_sql=f'select * from facility where facilityCode in ({rec[5]},{rec[6]},{rec[7]})'
            repCursor.execute(fac_sql)   #facilities fetched
            for f1,f2 in repCursor:
                fac.update({f1:f2.capitalize()})
            print('+','-'*98,'+',sep='')
            print('|','Sports Club'.center(96),'|')
            print('|','MEMBERSHIP CARD'.center(96),'|')
            date=datetime.datetime.now().strftime("%d/%m/%y") #date variable
            print('|',f'Member Code : {rec[0]}'.ljust(73),f'Date: {date}'.center(22),'|')
            print('|',f'Name        : {rec[1]}'.ljust(96),'|')
            print('|',f'Address     : {rec[3]}'.ljust(96),'|')
            print('|',f'Phone       : {rec[4]}'.ljust(48),f'Date of joining: {rec[2]}'.center(47),'|')
            print('|',f'Facilities Availed     : {fac[rec[5]]}, {fac[rec[6]]} and {fac[rec[7]]}'.ljust(96),'|')
            print('|',f'No. of Children Allowed: {rec[8]}'.ljust(96),'|')
            print('|',f'This card is valid only for 2 years from date of joining after that it should be renewed.'.ljust(96),'|')
            print('|',' '.center(96),'|')
            print('|','Authorised Signature   '.rjust(96),'|')
            print('+','-'*98,'+',sep='')
            t2=time.process_time()#time stops
            print(f'>>> {round(t2-t1,2)}s')
            
'''Main Executable'''
while True:
    print('''Main Menu [Make a number choice]:-
        1. Member Processing
        2. Fee Processing
        3. Facility Processing
        4. Reporting
        5. Exit''')
    mainChoice=int(input())
    #Processing Choices...
    if mainChoice==1:
        while True:
            print('''Member Menu [Make a number choice]:-
            1. New Member Registration
            2. Member Information Modification
            3. Deletion
            4. Member Details
            5. Return to Main Menu''')
            choice=int(input())
            #member choice processing...
            if   choice==1:
                MemberMenu.reg()
            elif choice==2:
                MemberMenu.mod()
            elif choice==3:
                MemberMenu.delt()
            elif choice==4:
                MemberMenu.det()
            elif choice==5:
                break
        
    elif mainChoice==2:
        while True:
            print('''Fee Processing Menu [Make a number choice]:-
            1. Entry of Fees
            2. Fee Details of a member
            3. Return to Main Menu''')
            choice=int(input())
            #fee choice processing...
            if   choice==1:
                FeeMenu.entry()
            elif choice==2:
                FeeMenu.det()
            elif choice==3:
                break
        
    elif mainChoice==3:
        while True:
            print('''Facility Processing Menu [Make a number choice]:-
            1. New Facility
            2. Facility Details
            3. Return to Main Menu''')
            choice=int(input())
            #facility choice processing...
            if   choice==1:
                FacilityMenu.new()
            elif choice==2:
                FacilityMenu.det()
            elif choice==3:
                break

    if mainChoice==4:
        while True:
            print('''Reporting Menu [Make a number choice]:-
            1. Members Details
            2. Activity Details
            3. Datewise Fee Details
            4. Overdue fee Details
            5. Membership card
            6. Return to Main Menu''')
            choice=int(input())
            #report choice processing...
            if   choice==1:
                ReportMenu.memberDetails()
            elif choice==2:
                ReportMenu.activityDetails()
            elif choice==3:
                ReportMenu.dwFeeDetails()
            elif choice==4:
                ReportMenu.odFeeDetails()
            elif choice==5:
                ReportMenu.memberCard()
            elif choice==6:
                break

    elif mainChoice==5:
        break
