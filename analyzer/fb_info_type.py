import os
import json
from sys import argv
import python_db
users = python_db.users
#some global variables
personalities = ['extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness']
extraversion_weights = {'user_events':0.4, 'user_checkins':0.9, 'user_groups':0.2, 'user_photo_video_tags':0.8, 'user_likes_per_status':0.9, 'user_comments_per_status':0.9, 'user_friends':0.9, 'user_friendlists':0.9}
agreeableness_weights = {'user_events':0.2, 'user_photo_video_tags':0.6, 'user_friends':0.7}
conscientiousness_weights = {'user_games_activity':0.8, 'user_groups':0.6, 'user_about_me':0.9, 'user_subscriptions':0.8}
neuroticism_weights = {'user_notes':0.7, 'user_status':0.8}
openness_weights = {'user_checkins':0.6, 'user_events':0.6, 'user_groups':0.4, 'user_likes':0.9, 'user_subscriptions':0.8, 'user_movies':0.2, 'user_music':0.2, 'user_television':0.2, 'user_books':0.2, 'user_games':0.2}

#fpath='./FBJ1/'
fpath='./subjects/'
# calculate the weights for features

def divide(x,y):
    if y!=0:
        return x / y
    else:
        return 0

def about_me_weight(userid):
    #filename = fpath+'users.u' + userid + '.me.json'
    #try:            
    #    about_me = json.loads(open(filename).read())
    #except IOError:
    #    return 0.0
    about_me=[s for s in users['u%s'%userid].me.find()][0]
    if 'quotes' in about_me:
        return 0.9
    return 0.0

def friends_weight(userid):
   # filename = fpath+'users.u' + userid + '.friends.json'
   # try:
   #     with open(filename) as f:
   #         friends = f.readlines()
   # except IOError:
   #     return 0.3    
   # friends = [json.loads(friend) for friend in friends]
    friends=[s for s in users['u%s'%userid].friends.find()]
    if len(friends) < 151:
        return 0.3
    if len(friends) < 601:
        return 0.6
    return 1.0

def friendlists_weight(userid):
   # filename = fpath+'users.u' + userid + '.friendlists.json'
   # try:
   #     with open(filename) as f:
   #         friendlists = f.readlines()
   # except IOError:
   #     return 0.3    
   # friendlists = [json.loads(friendlist) for friendlist in friendlists]
    friendlists=[s for s in users['u%s'%userid].friendlists.find()]
    if len(friendlists) < 6:
        return 0.3
    if len(friendlists) < 11:
        return 0.6
    return 1.0

def games_weight(userid):
   # filename = fpath+'users.u' + userid + '.games.json'
   # try:
   #     with open(filename) as f:
   #            games = f.readlines()
   # except IOError:
   #     return 0.3    
   # games = [json.loads(game) for game in games]
    games=[s for s in users['u%s'%userid].games.find()]
    if len(games) < 3:
        return 0.3
    if len(games) < 4:
        return 0.6
    return 1.0
    
def movies_weight(userid):
   # filename = fpath+'users.u' + userid + '.movies.json'
   # try:
   #     with open(filename) as f:
   #            movies = f.readlines()
   # except IOError:
   #     return 0.3    
    #movies = [json.loads(movie) for movie in movies]
    movies=[s for s in users['u%s'%userid].movies.find()]
    if len(movies) < 11:
        return 0.3
    if len(movies) < 21:
        return 0.6
    return 1.0

def music_weight(userid):
   # filename = fpath+'users.u' + userid + '.music.json'
   # try:
   #     with open(filename) as f:
   #            music = f.readlines()
   # except IOError:
   #     return 0.3    
    #music = [json.loads(m) for m in music]
    music =[s for s in users['u%s'%userid]. music.find()]
    if len(music) < 16:
        return 0.3
    if len(music) < 31:
        return 0.6
    return 1.0

def television_weight(userid):
   # filename = fpath+'users.u' + userid + '.television.json'
   # try:
   #     with open(filename) as f:
   #            television = f.readlines()
   # except IOError:
   #     return 0.3    
    #television = [json.loads(t) for t in television]
    television=[s for s in users['u%s'%userid].television.find()]
    if len(television) < 6:
        return 0.3
    if len(television) < 21:
        return 0.6
    return 1.0
    
def books_weight(userid):
   # filename = fpath+'users.u' + userid + '.books.json'
   # try:
   #     with open(filename) as f:
   #            books = f.readlines()
   # except IOError:
   #     return 0.3    
   # books = [json.loads(book) for book in books]
    books =[s for s in users['u%s'%userid].books.find()]
    if len(books) < 4:
        return 0.3
    return 1.0

def checkins_weight(userid):
   # filename = fpath+'users.u' + userid + '.checkins.json'
   # try:
   #     with open(filename) as f:
   #            checkins = f.readlines()
   # except IOError:
   #     return 0.3    
   # checkins = [json.loads(checkin) for checkin in checkins]
    checkins =[s for s in users['u%s'%userid].checkins.find()]
    if len(checkins) < 101:
        return 0.3
    if len(checkins) < 301:
        return 0.6
    return 1.0

def likes_weight(userid):
   # filename = fpath+'users.u' + userid + '.likes.json'
   # try:
   #     with open(filename) as f:
   #            likes = f.readlines()
   # except IOError:
   #     return 0.3    
   # likes = [json.loads(like) for like in likes]
    likes =[s for s in users['u%s'%userid].likes.find()]
    if len(likes) < 21:
        return 0.3
    if len(likes) < 61:
        return 0.6
    return 1.0

def events_weight(userid):
   # filename = fpath+'users.u' + userid + '.events.json'
   # try:
   #     with open(filename) as f:
   #            events = f.readlines()
   # except IOError:
   #     return 0.3    
   # events = [json.loads(event) for event in events]
    events =[s for s in users['u%s'%userid].events.find()]
    if len(events) < 11:
        return 0.3
    if len(events) < 36:
        return 0.6
    return 1.0

def groups_weight(userid):
   # filename = fpath+'users.u' + userid + '.groups.json'
   # try:
   #     with open(filename) as f:
   #            groups = f.readlines()
   # except IOError:
   #     return 0.3    
   # group = [json.loads(group) for group in groups]
    groups=[s for s in users['u%s'%userid].groups.find()]
    if len(groups) < 4:
        return 0.3
    if len(groups) < 11:
        return 0.6
    return 1.0
    
def notes_weight(userid):
   # filename = fpath+'users.u' + userid + '.notes.json'
   # try:
   #     with open(filename) as f:
   #            notes = f.readlines()
   # except IOError:
   #     return 0.3    
   # notes = [json.loads(note) for note in notes]
    notes =[s for s in users['u%s'%userid].notes.find()]
    if len(notes) < 4:
        return 0.3
    if len(notes) < 11:
        return 0.6
    return 1.0

def statuses_per_month_weight(userid):
   # filename = fpath+'users.u' + userid + '.statuses.json'
   # try:
   #     with open(filename) as f:
   #            statuses = f.readlines()
   # except IOError:
   #     return 0.3    
   # statuses = [json.loads(status) for status in statuses]
    statuses =[s for s in users['u%s'%userid].statuses.find()]
    if len(statuses)>0:
        last_status = statuses[0]
        last_date = last_status['updated_time']
        last_year = int(last_date[:4])
        last_month = int(last_date[5:7])
            
        first_status = statuses[len(statuses) - 1]
        first_date = last_status['updated_time']
        first_year = int(last_date[:4])
        first_month = int(last_date[5:7])
        
        number_of_months = 0
        if first_month < last_month:
            number_of_months = (last_year - first_year) * 12 + (last_month - first_month) + 1
        else:
            number_of_months = (last_year - first_year) * 12 - (last_month - first_month) + 1
                
        posts_per_month = divide(len(statuses),number_of_months)
        if posts_per_month < 13:
            return 0.3
        if posts_per_month < 21:
            return 0.6
        return 1.0
    else:
         return 0.3
    
def likes_per_status_weight(userid):
   # filename = fpath+'users.u' + userid + '.statuses.json'
   # try:
   #     with open(filename) as f:
   #            statuses = f.readlines()
   # except IOError:
   #     return 0.3    
   # statuses = [json.loads(status) for status in statuses]
    statuses =[s for s in users['u%s'%userid].statuses.find()]
    likes = 0
    for status in statuses:
        if 'likes' in status:
            likes += len(status['likes']['data'])
    likes_per_status = divide(likes,len(statuses))
    if likes_per_status < 13:
        return 0.3
    if likes_per_status < 21:
        return 0.6
    return 1.0
    
def comments_per_status_weight(userid):
   # filename = fpath+'users.u' + userid + '.statuses.json'
   # try:
   #     with open(filename) as f:
   #            statuses = f.readlines()
   # except IOError:
   #     return 0.3    
   # statuses = [json.loads(status) for status in statuses]
    statuses =[s for s in users['u%s'%userid].statuses.find()]
    comments = 0
    for status in statuses:
        if 'comments' in status:
            comments += len(status['comments']['data'])
    if divide(comments,len(statuses)) < 6:
        return 0.3
    if divide(comments,len(statuses)) < 16:
        return 0.6
    return 1.0

def videos_weight(userid):
   # filename = fpath+'users.u' + userid + '.videos.json'
   # try:
   #     with open(filename) as f:
   #            videos = f.readlines()
   # except IOError:
   #     return 0.3    
   # videos = [json.loads(video) for video in videos]
    videos =[s for s in users['u%s'%userid]. videos.find()]
    if len(videos) < 6:
        return 0.3
    if len(videos) < 16:
        return 0.6
    return 1.0

def tagged_weight(userid):
   # filename = fpath+'users.u' + userid + '.tagged.json'
   # try:
   #     with open(filename) as f:
   #            tagged = f.readlines()
   # except IOError:
   #     return 0.3    
   # tagged = [json.loads(t) for t in tagged]
    tagged =[s for s in users['u%s'%userid]. tagged.find()]
    tagged = [tag for tag in tagged if tag['created_time'][:4] == '2013']
    if len(tagged) < 61:
        return 0.3
    if len(tagged) < 301:
        return 0.6
    return 1.0

def subscriptions_weight(userid):
   # filename = fpath+'users.u' + userid + '.subscriptions.json'
   # try:
   #     with open(filename) as f:
   #            subscriptions = f.readlines()
   # except IOError:
   #     return 0.3    
   # subscriptions = [json.loads(subscription) for subscription in subscriptions]
    subscriptions =[s for s in users['u%s'%userid].subscriptions.find()]
    #it was mentioned just to count the subscriptions in 2013, but that information is not available
    if len(subscriptions) < 13:
        return 0.3
    if len(subscriptions) < 49:
        return 0.6
    return 1.0

# get the userids from all the files in the folder
#def get_userids():
#    filenames = [f for f in os.listdir('.') if os.path.isfile(f)]
#    #print 'filename:',filenames
#    userids = []
#    for filename in filenames:
#        if filename[:6] == 'users.':    #filter out all the other files
#            filename = filename[7:]
#            if filename[:5] == '10000':
#                filename = filename[:15]
#            else:
#                filename = filename[:10]
#            userids.append(filename)
#    return set(userids)

# calculation of the different personalities
def calc_extraversion(userids):
    events_calculated_weight = 0
    checkins_calculated_weight = 0
    groups_calculated_weight = 0
    tags_calculated_weight = 0
    likes_per_status_calculated_weight = 0
    comments_per_status_calculated_weight = 0
    friends_calculated_weight = 0
    friendlists_calculated_weight = 0
    for userid in userids:
        events_calculated_weight += extraversion_weights['user_events'] * events_weight(userid)
        checkins_calculated_weight += extraversion_weights['user_checkins'] * checkins_weight(userid)
        groups_calculated_weight += extraversion_weights['user_groups'] * groups_weight(userid)
        tags_calculated_weight += extraversion_weights['user_photo_video_tags'] * tagged_weight(userid)
        likes_per_status_calculated_weight += extraversion_weights['user_likes_per_status'] * likes_per_status_weight(userid)
        comments_per_status_calculated_weight += extraversion_weights['user_comments_per_status'] * comments_per_status_weight(userid)
        friends_calculated_weight += extraversion_weights['user_friends'] * friends_weight(userid)
        friendlists_calculated_weight += extraversion_weights['user_friendlists'] * friendlists_weight(userid)
    userid_count = len(userids)
    events_calculated_weight=divide(events_calculated_weight,userid_count)
    checkins_calculated_weight=divide(checkins_calculated_weight,userid_count)
    groups_calculated_weight=divide(groups_calculated_weight,userid_count)
    tags_calculated_weight=divide(tags_calculated_weight,userid_count)
    likes_per_status_calculated_weight=divide(likes_per_status_calculated_weight,userid_count)    
    comments_per_status_calculated_weight=divide(comments_per_status_calculated_weight,userid_count)
    friends_calculated_weight=divide(friends_calculated_weight,userid_count)
    friendlists_calculated_weight=divide(friendlists_calculated_weight,userid_count)
    average = ((events_calculated_weight + checkins_calculated_weight + groups_calculated_weight + tags_calculated_weight + likes_per_status_calculated_weight + comments_per_status_calculated_weight + friends_calculated_weight + friendlists_calculated_weight) / 19) / sum(extraversion_weights.values())
    #print "Extraversion:"
    #print "Events weight:", events_calculated_weight
    #print "Checkins weight:", checkins_calculated_weight
    #print "Groups weight:", groups_calculated_weight
    #print "Tags weight:", tags_calculated_weight
    #print "Likes per status weight:", likes_per_status_calculated_weight
    #print "Comments per status weight:", comments_per_status_calculated_weight
    #print "Friends weight:", friends_calculated_weight
    #print "Friendlists weight:", friendlists_calculated_weight
    return average
    
def calc_agreeableness(userids):
    events_calculated_weight = 0
    tags_calculated_weight = 0
    friends_calculated_weight = 0
    for userid in userids:
        events_calculated_weight += agreeableness_weights['user_events'] * events_weight(userid)
        tags_calculated_weight += agreeableness_weights['user_photo_video_tags'] * tagged_weight(userid)
        friends_calculated_weight += agreeableness_weights['user_friends'] * friends_weight(userid)
    userid_count = len(userids)
    events_calculated_weight=divide(events_calculated_weight,userid_count)
    tags_calculated_weight=divide(tags_calculated_weight,userid_count)
    friends_calculated_weight=divide(friends_calculated_weight,userid_count)
    average = ((events_calculated_weight + tags_calculated_weight + friends_calculated_weight) / 19) / sum(agreeableness_weights.values())
    #print "Agreeableness:"
    #print "Events weight:", events_calculated_weight
    #print "Tags weight:", tags_calculated_weight
    #print "Friends weight:", friends_calculated_weight
    return average

def calc_conscientiousness(userids):
    games_activity_calculated_weight = 0
    groups_calculated_weight = 0
    about_me_calculated_weight = 0
    subscriptions_calculated_weight = 0
    for userid in userids:
        games_activity_calculated_weight += conscientiousness_weights['user_games_activity'] * games_weight(userid)
        groups_calculated_weight += conscientiousness_weights['user_groups'] * groups_weight(userid)
        about_me_calculated_weight += conscientiousness_weights['user_about_me'] * about_me_weight(userid)
        subscriptions_calculated_weight += conscientiousness_weights['user_subscriptions'] * subscriptions_weight(userid)
    userid_count = len(userids)
    games_activity_calculated_weight=divide(games_activity_calculated_weight,userid_count)
    groups_calculated_weight=divide(groups_calculated_weight,userid_count)
    about_me_calculated_weight=divide(about_me_calculated_weight,userid_count)
    subscriptions_calculated_weight=divide(subscriptions_calculated_weight,userid_count)
    average = divide(((games_activity_calculated_weight + groups_calculated_weight + about_me_calculated_weight + subscriptions_calculated_weight) / 19) , sum(conscientiousness_weights.values()))
    #print "Conscientiousness:"
    #print "Games weight:", games_activity_calculated_weight
    #print "Groups weight:", groups_calculated_weight
    #print "About me weight:", about_me_calculated_weight    
    #print "Subscriptions weight:", subscriptions_calculated_weight
    return average
    
def calc_neuroticism(userids):
    notes_calculated_weight = 0
    statuses_per_month_calculated_weight = 0
    for userid in userids:
        notes_calculated_weight += neuroticism_weights['user_notes'] * notes_weight(userid)
        statuses_per_month_calculated_weight += neuroticism_weights['user_status'] * statuses_per_month_weight(userid)
    userid_count = len(userids)
    notes_calculated_weight=divide(notes_calculated_weight,userid_count)
    statuses_per_month_calculated_weight=divide(statuses_per_month_calculated_weight,userid_count)
    average = ((notes_calculated_weight + statuses_per_month_calculated_weight) / 19) / sum(neuroticism_weights.values())
    #print "Neuroticism:"
    #print "Notes weight:", notes_calculated_weight
    #print "Statuses weight:", statuses_per_month_calculated_weight
    return average

def calc_openness(userids):
    checkins_calculated_weight = 0
    events_calculated_weight = 0
    groups_calculated_weight = 0
    likes_calculated_weight = 0
    subscriptions_calculated_weight = 0
    movies_calculated_weight = 0
    music_calculated_weight = 0
    television_calculated_weight = 0
    books_calculated_weight = 0
    games_calculated_weight = 0
    for userid in userids:
        checkins_calculated_weight += openness_weights['user_checkins'] * checkins_weight(userid)
        events_calculated_weight += openness_weights['user_events'] * events_weight(userid)
        groups_calculated_weight += openness_weights['user_groups'] * groups_weight(userid)
        likes_calculated_weight += openness_weights['user_likes'] * likes_weight(userid)
        subscriptions_calculated_weight += openness_weights['user_subscriptions'] * subscriptions_weight(userid)
        movies_calculated_weight += openness_weights['user_movies'] * movies_weight(userid)
        music_calculated_weight += openness_weights['user_music'] * music_weight(userid)
        television_calculated_weight += openness_weights['user_television'] * television_weight(userid)
        books_calculated_weight += openness_weights['user_books'] * books_weight(userid)
        games_calculated_weight += openness_weights['user_games'] * games_weight(userid)
    userid_count = len(userids)
    checkins_calculated_weight=divide(checkins_calculated_weight,userid_count)
    events_calculated_weight=divide(events_calculated_weight,userid_count)
    groups_calculated_weight=divide(groups_calculated_weight,userid_count)
    likes_calculated_weight=divide(likes_calculated_weight,userid_count)
    subscriptions_calculated_weight=divide(subscriptions_calculated_weight,userid_count)
    movies_calculated_weight=divide(movies_calculated_weight,userid_count)
    music_calculated_weight=divide(music_calculated_weight,userid_count)
    television_calculated_weight=divide(television_calculated_weight,userid_count)
    books_calculated_weight=divide(books_calculated_weight,userid_count)
    games_calculated_weight=divide(games_calculated_weight,userid_count)
    average = divide(((checkins_calculated_weight + events_calculated_weight + groups_calculated_weight + likes_calculated_weight + subscriptions_calculated_weight + movies_calculated_weight + music_calculated_weight + television_calculated_weight + books_calculated_weight + games_calculated_weight) / 19) , sum(openness_weights.values()))
    #print "Openness:"
    #print "Checkins weight:", checkins_calculated_weight
    #print "Events weight:", events_calculated_weight
    #print "Groups weight:", groups_calculated_weight
    #print "Likes weight:", likes_calculated_weight
    #print "Subscriptions weight:", subscriptions_calculated_weight
    #print "Movies weight:", movies_calculated_weight
    #print "Music weight:", music_calculated_weight
    #print "Television weight:", television_calculated_weight
    #print "Books weight:", books_calculated_weight
    #print "Games weight:", games_calculated_weight
    return average 


# the basic program flow
#userid = raw_input("If you want your data computed, type in your userid. To get the average, type in 'all'\n")
#if userid == 'all':
#    userids = get_userids()
#else:
def main():
    userids = [argv[1]]
    extraversion_average = calc_extraversion(userids)
    agreeableness_average = calc_agreeableness(userids)
    conscientiousness_average = calc_conscientiousness(userids)
    neuroticism_average = calc_neuroticism(userids)
    openness_average = calc_openness(userids)
    average_sum = extraversion_average + agreeableness_average + conscientiousness_average + neuroticism_average + openness_average
    extraversion_average=divide(extraversion_average,average_sum)
    agreeableness_average=divide(agreeableness_average,average_sum)
    conscientiousness_average=divide(conscientiousness_average,average_sum)
    neuroticism_average=divide(neuroticism_average,average_sum)
    openness_average=divide(openness_average,average_sum)
    #print "Average values", "\nExtraversion:", extraversion_average, "\nAgreeableness:", agreeableness_average, "\nConscientiousness:", conscientiousness_average, "\nNeuroticism:", neuroticism_average, "\nOpenness:", openness_average
    print '{"EXT":%f,"AGR":%f,"CON":%f,"NEO":%f,"OPE":%f}'%(extraversion_average,agreeableness_average,conscientiousness_average,neuroticism_average,openness_average)
if __name__=="__main__":
    main()
