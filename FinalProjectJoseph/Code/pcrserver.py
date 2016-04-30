###########################################################################################
# Author: Josh Joseph joshmd@bu.edu
# 4/29/16
# This is the main server file for PCR hero....

from bottle import route, run, template, get, post, request, response, redirect, static_file
import pcrlib
import os

pcrDB = pcrlib.get_db("pcrhero")
HASHWORD = 'applesauce'
HOSTIP = 'http://www.pcrhero.org:8000'
HOMEDIR = '/home/ubuntu/pythonproject/'

###########################################################################################
### File get path functions -- This section can be cleaned up if all file requests are listed
### with their appropriate file path after the root directory...  #TODO
############################################################################################

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/static/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/badges/<filename:path>')
def badge(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/badges/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/issuers/<filename:path>')
def issuer(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/issuers/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/users/<filename:path>')
def issuer(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/users/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/images/<filename:path>')
def image(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/images/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/criteria/<filename:path>')
def criteria(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/criteria/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host

@get('/awardedbadges/<filename:path>')
def awardedbadge(filename):
    return static_file(filename, root='/home/ubuntu/pythonproject/awardedbadges/')
    ##This is a filepath to static addresses on the site. You will need to use an appropriate
    ##address (or a system link for security purposes) when using on a different host



##########################################################################################
#### MAIN ROUTING FUNCTIONS
##########################################################################################


@route('/')
def home():
    return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h1>PCR Hero - your journey to achievement begins here!</h1>
</body>
'''


####################### TO DO - put remainder of register logic into a tpl file rather than expanding here

@get('/register')
def show_registration():
    return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h1>Thanks for registering with PCR Hero - your journey to achievement begins here!</h1>
<form action="" method="POST">
    <p>
    <label for="name">What is your name?</label>
    <input type="text" name="name"/> </p>
    <p>
    <label for="email">What is your email?</label>
    <input type="email" name="email"/> </p>
    <p>
    <label for="password">Enter a strong password:</label>
    <input type="password" name="password"/> </p>
    <p>
    <label for="password">Reenter that strong password:</label>
    <input type="password" name="passwordcheck"/> </p>
    <input type="submit"/>
</form>
</body>
'''

@post('/register')
def show_name():
    name = request.params.name
    email = request.params.email
    password = request.params.password
    passwordcheck = request.params.passwordcheck
    if(password != passwordcheck):
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
    <h1>Thanks for registering with PCR Hero - your journey to achievement begins here!</h1>
    <form action="" method="POST">
        <p>
        <label for="name">What is your name?</label>
        <input type="text" name="name" required/> </p>
        <p>
        <label for="email">What is your email?</label>
        <input type="email" name="email" required/> </p>
        <p>
        <label for="password">Enter a strong password:</label>
        <input type="password" name="password" required/> </p>
        <p>
        <label for="password">Reenter that strong password:
        <input type="password" name="passwordcheck" required/> 
        <div style = "color: red; display: inline;"> Passwords need to match! </div> </label></p>
        <input type="submit"/>
    </form>
    </body>
    '''
    elif(pcrlib.get_person(pcrDB, email) != None):
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
    <h1>Thanks for registering with PCR Hero - your journey to achievement begins here!</h1>
    <form action="" method="POST">
        <p>
        <label for="name">What is your name?
        <input type="text" name="name"/> 
        </label></p>
        <p>
        <label for="email">What is your email?</label>
        <input type="email" name="email" required/> 
        <div style = "color: red; display: inline;"> That email is taken! </div></p>
        <p>
        <label for="password">Enter a strong password:</label>
        <input type="password" name="password" required/> </p>
        <p>
        <label for="password">Reenter that strong password:</label>
        <input type="password" name="passwordcheck" required/> 
        </p>
        <input type="submit"/>
    </form>
    </body>
    '''    
    else:
        ## It worked!
        ## Hash the password
        hashword = pcrlib.shaHash(password, "deadsea")
        ## create the new user object
        newUser = pcrlib.PCRUser(email, name, hashword)
        pcrlib.add_person(pcrDB, newUser)
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h2>Hello, {}!</h2><p>Thanks for registering.</p>
</body>
</html>
'''.format(request.POST.name)


########## END TODO (reminder, putting this in a tpl will save like ~70 lines of code :)


@get('/myprofile')
def profile():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        userapps = pcrlib.get_users_apps(pcrDB, useremail)
        applist = {}
        for appname in userapps:
            applist[appname] = (pcrlib.get_app(pcrDB, appname))

        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero - {}</h1>
        '''.format(useremail) + template('profile.tpl', badges=userbadges, apps=applist) + "</body>"
    else:
        redirect("/login")



@get('/login')
def show_registration():
    return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + '''\
<h1>Welcome to PCR Hero - please login here!</h1>
<form action="" method="POST">
    <p>
    <label for="email">Email:</label>
    <input type="email" name="email" required/> </p>
    <p>
    <label for="password">Password:</label>
    <input type="password" name="password" required/> </p>
    <p>
    <input type="submit"/>
</form>
</body>
'''

@post('/login')
def show_name():
    email = request.params.email
    password = request.params.password
    hashword = pcrlib.shaHash(password, "deadsea")
    ### need to begin with checking for username (email) - otherwise we'll get a keyerror
    if(pcrlib.get_person(pcrDB, email) == None):
        return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + "Sorry - this username is not registered!"
    else:
        ### need to load up the user's hashword for comparison purposes
        loginHashword = pcrlib.get_user_hashword(pcrDB, email)
        if(hashword != loginHashword):
            return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + "Sorry - your password is incorrect!"
        elif(hashword == loginHashword):
            response.set_cookie('loggedin', email, max_age= 600, secret='applesauce', path='/')
            return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce')) + "<h2>Hello, {}!<p>Welcome back!</p></h2>".format(request.POST.email)
        else:
            return template('base.tpl', title='PCR Hero', email=request.get_cookie('loggedin', secret='applesauce'))+ "Sorry, something went wrong!"



@get('/admin-badge')
def badge_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        issuers = pcrlib.get_issuers(pcrDB)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-badge.tpl', badges=userbadges, issuers=issuers, images=available_images) + "</body>"
    else:
        redirect("/login")

@post('/admin-badge')
def badge_submit():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        issuers = pcrlib.get_issuers(pcrDB)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)
        
        ## return args
        name = request.params.name
        if(pcrlib.find_badge(pcrDB, name) != None):
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:red">A badge with that name already exists!</h2>
            '''.format(useremail) + template('admin-badge.tpl', badges=userbadges, issuers=issuers, images=available_images) + "</body>"

        else:
            description = request.params.description
            image = request.params.image
            criteria = request.params.criteria
            tags = request.params.tags
            issuer = request.params.issuer

            newBadge = pcrlib.OpenBadge(name, description, image, criteria, tags, issuer)
            newBadge.establish_here()
            newBadge.add_badge(pcrDB)

            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:blue">Your badge was successfully created!</h2>
            '''.format(useremail) + template('admin-badge.tpl', badges=userbadges, issuers=issuers, images=available_images) + "</body>"

    else:
        redirect("/login")

@get('/admin-issuer')
def issuer_create_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        issuers = pcrlib.get_issuers(pcrDB)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-issuer.tpl', badges=userbadges, issuers=issuers) + "</body>"
    else:
        redirect("/login")

@post('/admin-issuer')
def issuer_create_submit():
    name = request.params.name
    description = request.params.description
    url = request.params.url
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        issuers = pcrlib.get_issuers(pcrDB)
        if(pcrlib.find_issuer(pcrDB, name) != None):
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1> <p style="color:red;">Sorry, that issuer is taken!</p>
            '''.format(useremail) + template('admin-issuer.tpl', badges=userbadges, issuers=issuers) + "</body>"
        else:
            newIssuer = pcrlib.PCRIssuer(name, description, url)
            pcrlib.add_issuer(pcrDB, newIssuer)
            newIssuer.establish_here()
            issuers = pcrlib.get_issuers(pcrDB)
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1> <p style="color:blue;">Your issuer has been created!</p>
            '''.format(useremail) + template('admin-issuer.tpl', badges=userbadges, issuers=issuers) + "</body>"
    else:
        redirect("/login")


@get('/admin-awards')
def badge_award_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        badge_list = pcrlib.get_badges(pcrDB)
        user_list = pcrlib.get_users(pcrDB)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-award.tpl', badges=badge_list, users=user_list) + "</body>"
    else:
        redirect("/login")

@post('/admin-awards')
def badge_award_submit():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        badge_list = pcrlib.get_badges(pcrDB) # list of all badges
        user_list = pcrlib.get_users(pcrDB) # list of all users
        current_user = request.params.user
        current_user_badges = pcrlib.get_users_badges(pcrDB, current_user)
        current_badge = request.params.badge
        ## check that the user doesn't already have the badge
        # if so, send back to the menu
        if(current_badge in current_user_badges):
             return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:red;">That user already has that badge!</h2>
            '''.format(useremail) + template('admin-award.tpl', badges=badge_list, users=user_list) + "</body>"           
        # if not, award the badge
        ## awarding badge magic
        else:
            pcrlib.award_badge_to_user(pcrDB, current_badge, current_user)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
            <h2 style="color:blue;">Badge successfully awarded!<h2>
        '''.format(useremail) + template('admin-award.tpl', badges=badge_list, users=user_list) + "</body>"
    else:
        redirect("/login")



@get('/admin-images')
def images_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-images.tpl', badges=userbadges, images=available_images, image_path=image_path) + "</body>"
    else:
        redirect("/login")

@post('/admin-images')
def upload_image():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        userbadges = pcrlib.get_users_badges(pcrDB, useremail)
        image_path = "/home/ubuntu/pythonproject/images"
        available_images = os.listdir(image_path)

        upload = request.files.image
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.png'):
            return "File extension not allowed."

        save_path = "/home/ubuntu/pythonproject/images"

        file_path = "{path}/{file}".format(path=save_path, file=upload.filename)
        upload.save(file_path)


        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
            <h2 style="color:blue">Image successfully uploaded!</h2>
        '''.format(useremail) + template('admin-images.tpl', badges=userbadges, images=available_images, image_path=image_path) + "</body>"
    else:
        redirect("/login")


@get('/admin-tasks')
def tasks_menu():
    if(request.get_cookie('loggedin')):
        useremail = request.get_cookie('loggedin', secret='applesauce')
        badge_list = pcrlib.get_badges(pcrDB)
        user_list = pcrlib.get_users(pcrDB)
        return template('base.tpl', title='PCR Hero', email= useremail) + '''\
            <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
        '''.format(useremail) + template('admin-tasks.tpl', badges=badge_list, users=user_list, typeselection = 0) + "</body>"
    else:
        redirect("/login")

@post('/admin-tasks')
def tasks_menu_post():
    if(request.get_cookie('loggedin')):
        submitted = request.params.flag
        typeselection = request.params.typeselection
        badge_list = pcrlib.get_badges(pcrDB)
        user_list = pcrlib.get_users(pcrDB)
        app_list = pcrlib.get_all_apps(pcrDB)
        useremail = request.get_cookie('loggedin', secret='applesauce')
        if(submitted == "False"):
            if(typeselection != 0):
                app = request.params.app
            return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
            '''.format(useremail) + template('admin-tasks.tpl', badges=badge_list, users=user_list, app_list=app_list, typeselection = typeselection, app = app) + "</body>"
        else:
            user = request.params.user
            badge = request.params.badge
            app = request.params.app
            print("typeselection = %s " % typeselection)
            ### type handling for task assignment:
            if(typeselection == "percent"):
                circuit = request.params.circuit
                score = float(request.params.score)
                percent = int(request.params.percent)
                NewTask = pcrlib.PercentTask(user, badge, app, circuit, score, percent)

            elif(typeselection == "repeat"):
                circuit = request.params.circuit
                repeat = int(request.params.repeat)
                NewTask = pcrlib.RepeatTask(user, badge, app, circuit, repeat)

            elif(typeselection == "unique"):
                unique = request.params.unique
                NewTask = pcrlib.UniqueTask(user, badge, app, unique)

            elif(typeselection == "timetrial"):
                days = int(request.params.days)
                hours = int(request.params.hours)
                minutes = int(request.params.minutes)
                circuit = request.params.circuit
                tasknum = int(request.params.tasknum)
                NewTask = pcrlib.TimeTrialTask(user, badge, app, days, hours, minutes, circuit, tasknum)

            else: #performance
                circuit = request.params.circuit
                targetyield = int(request.params.targetyield)
                cost = int(request.params.cost)
                NewTask = pcrlib.PerformanceTask(user, badge, app, circuit, targetyield, cost)

            ### task is assigned, now time to see if it's unique...
            print(NewTask.output())
            result = NewTask.assign(pcrDB)

            if(result):
                return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                <h2 style="color:blue;">Task successfully started...</h2>
            '''.format(useremail) + template('admin-tasks.tpl', badges=badge_list, users=user_list, typeselection = 0) + "</body>"
            else:
                return template('base.tpl', title='PCR Hero', email= useremail) + '''\
                    <h1>Welcome to PCR Hero's Admin Menu - {}</h1>
                    <h2 style="color:red;">Task already assigned to user...</h2>
                '''.format(useremail) + template('admin-tasks.tpl', badges=badge_list, users=user_list, typeselection = 0) + "</body>"
    else:
        redirect("/login")

@post('/submit')
def submit():
    username = request.params.user
    appname = request.params.app
    submittedcircuit = request.params.circuit
    tasks = pcrlib.get_users_tasks_for_app(pcrDB, username, appname)
    taskarray = []
    for task in tasks:
        taskarray.append(task)
    print('TaskList----')
    for task in taskarray:
        print(task)

    print('\n')

    # Step 1 - evaluate for tasks that have expired and remove them (time trials)
    print('Check for timetrials...')
    for task in taskarray:
        if(task['type'] == 'timetrial'):
            if(pcrlib.check_task_datetime(pcrDB, task)):
                ## check_task_datetime returns True if time's up
                print("%s's time is up!" % task['badge'])
                pcrlib.remove_task_by_id(pcrDB, task['_id']) ## delete task now that badge has been awarded
                taskarray.remove(task) ## remove from taskarray
                print("Task removed...")

    # # Step 2 - evaluate badges and award them if completed
    # ### Step 3 - evaluate for tasks that need unique submissions or multiple tasks (unique, repeat, timetrial)
    for task in taskarray:
        if(task['type'] == 'unique'):
            pass ## This is the one circuit type that is going to require a little more work
            ## What is needed is for a mongodb call to $find the {circuit: circuit name} in the 

        elif(task['type'] == 'repeat'):
            if(task['circuit'] == submittedcircuit):
                pcrlib.increment_task_by_id(pcrDB, task['_id'], "count")
                ## check if criteria met...
                if(task['count'] >= task['repeatTarget']):
                    pcrlib.award_badge_to_user(pcrDB, task['badge'], task['user'])
                    print("A new badge was awarded to %s!" % task['user'])
                    pcrlib.remove_task_by_id(pcrDB, task['_id']) ## delete task now that badge has been awarded
                    taskarray.remove(task) ## remove from taskarray
                    print("Task removed...")

        elif(task['type'] == 'timetrial'):
            if(task['circuit'] == submittedcircuit):
                pcrlib.increment_task_by_id(pcrDB, task['_id'], "tasksDone")

                ## check if criteria met...
                if(task['tasksDone'] >= task['tasknumGoal']):
                    pcrlib.award_badge_to_user(pcrDB, task['badge'], task['user'])
                    print("A new badge was awarded to %s!" % task['user'])
                    pcrlib.remove_task_by_id(pcrDB, task['_id']) ## delete task now that badge has been awarded
                    taskarray.remove(task) ## remove from taskarray
                    print("Task removed...")

    ### Step 4 - compare percentage scores

        elif(task['type'] == 'percent'):
            if(task['circuit'] == submittedcircuit):
                newScore = reqeust.params.score
                ## check if criteria met...
                if(newScore >= task['goalScore']):
                    pcrlib.award_badge_to_user(pcrDB, task['badge'], task['user'])
                    print("A new badge was awarded to %s!" % task['user'])
                    pcrlib.remove_task_by_id(pcrDB, task['_id']) ## delete task now that badge has been awarded
                    taskarray.remove(task) ## remove from taskarray
                    print("Task removed...")

                ## else, check if this is an improvement - this will be useful once the tasks badge is implemented
                if(newScore >= task['score']):
                    pcrlib.update_task_by_id(pcrDB, task['_id'], "score", newScore)
                    print("Score improved! Getting closer!")

    ### Step 5 - check cost/performance scores
        elif(task['type'] == 'performance'):
            if(task['circuit'] == submittedcircuit):
                newScore = reqeust.params.score
                newCost = request.params.cost
                ## check if criteria met...
                if(newScore >= task['targetyield']):
                    if(newCost <= task['cost']):
                        pcrlib.award_badge_to_user(pcrDB, task['badge'], task['user'])
                        print("A new badge was awarded to %s!" % task['user'])
                        pcrlib.remove_task_by_id(pcrDB, task['_id']) ## delete task now that badge has been awarded
                        taskarray.remove(task) ## remove from taskarray
                        print("Task removed...")

        else:
            pass  ## can always add new task types

@get('/logout')
def logout():
    response.set_cookie('loggedin', '', path='/')
    redirect("/")

run(host='172.31.57.1', port=8000, debug=True)
