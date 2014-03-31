#!//usr/bin/python
from functools import partial
from facebook import FacebookAPI, GraphAPI
import facebook
from pprint import pprint
import time
import json
import sys
import re
import random
import string
#import python_db

_CRAWL_ALL = True

def read_key():
    f=open("../key/keyfile.json",'r')
    key_string="".join([l.strip() for l in f.readlines()])
    #print key_string
    key=json.loads(key_string)
    f.close()
    return key['key']

#users = python_db.users
_DIR_KEY=read_key()


def get_paging_parameters(url):
    actionparams_list = re.findall(r'\w+=\w+', url)
    actionparams = {}     
    for p in actionparams_list:
        ent = p.split('=')
        if ent[0] != 'access_token':
            actionparams[ent[0]] = ent[1]

    return actionparams


def gen_key(k_len):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(k_len))

def save_score(uid,score):
    file_key=gen_key(10)
    fw=open("./subjects_%s/users.u%s.%s.%s.json"%(_DIR_KEY,uid,'score',file_key),'w')
    fw.write(json.dumps({'score':score}))
    fw.close()


def save_one_user_graph_data( uid, graph, last_start_time_str, action): 
    #print ' action = ' + action

    file_key=gen_key(10)
    #file_key='JC38W2CE'
    fw=open("./subjects_%s/users.u%s.%s.%s.json"%(_DIR_KEY,uid,action,file_key),'w')
    #user = users['u%s' % uid]
    fwlist=[]

    if last_start_time_str:
        last_start_time = time.strptime(last_start_time_str, '%Y-%m-%dT%H:%M:%S')

    if not action or action == 'me':
        target_to_get = 'me'
        time_field_to_check = 'updated_time'
    else:
        target_to_get = 'me/%s' % action
        time_field_to_check = 'created_time'

    graph_paging_next_params = {}
    while True:
        got_old_post = False
        try:
            graph_result = graph.get(target_to_get, params=graph_paging_next_params)
        except facebook.GraphAPIError as grapherr:
            #print grapherr.decode('utf-8')
            fw.write('\n'.join(fwlist))
            fw.close()
            return

        # if action is just me, add the whole result directly
        if target_to_get == 'me':
            #print graph_result #savesave
            fwlist.append(json.dumps(graph_result))
            #user.me.update({time_field_to_check : graph_result[time_field_to_check]}, graph_result, upsert = True)
            break
        
        if 'data' in graph_result:
            graph_data = graph_result['data']
        else:
            print 'cannot get %s data from graph API' % target_to_get
            fw.write('\n'.join(fwlist))
            fw.close()
            return

        if 'paging' in graph_result and 'next' in graph_result['paging']:
            graph_paging_next_params = get_paging_parameters(graph_result['paging']['next'])
        else:
            graph_paging_next_params = None

        item_saved_count = 0
        for item in graph_data:
            final_field_to_check = time_field_to_check 
            if last_start_time_str and time_field_to_check in item: # any time field exists ?
                # convert current data's time string to struct_time
                # original format: '2012-11-24T17:17:17+0000'
                # so we skip the last 5 characters
                post_time = time.strptime(item[time_field_to_check][:-5], '%Y-%m-%dT%H:%M:%S')
                if post_time <= last_start_time:
                    print '  got old post at %s, older than %s, skip' % (item[time_field_to_check][:-5], last_start_time_str)
                    got_old_post = True
                    break
            else:
                final_field_to_check = 'id'
            
            #user[action].update({final_field_to_check : item[final_field_to_check]}, item, upsert = True)
            #print item #savesave
            fwlist.append(json.dumps(item))
            #user[action].update({final_field_to_check : item[final_field_to_check]}, item, upsert = True)
            item_saved_count += 1

        print '  %d items saved' % item_saved_count

        # determine if next round needed
        if not _CRAWL_ALL or not graph_paging_next_params or got_old_post:
            break
        print '  next round:', graph_paging_next_params

    #print ' done saving action "%s", all %d item(s)\n' % (action, user[action].count())
    fw.write('\n'.join(fwlist))
    fw.close()
    print ' done saving action "%s"' % (action)


def save_one_user(access_token_data):
    access_token = access_token_data['access_token']
    uid = access_token_data['uid']
    #score = access_token_data['score']
    #print uid
    #time_field = access_token_data.get('crawl_start_time') 

    #users.score.update({'uid':uid},{'uid':uid,'score':score,'time':time_field} , upsert = True)
    #print 'current count of feed,likes,notes: %d,%d,%d' % \
    #      (user.feed.count(), user.likes.count(), user.notes.count())
 
    if not access_token or access_token_data.get('need_crawl', '1') == '0':    
        # default to crawl, except explicitly set don't-crawl
        if not access_token:
            print 'no access token for %s(%s)' % (access_token_data['uid'], uid)
        if access_token_data.get('need_crawl', '1') == '0':
            print 'no new crawling request'

        lasttime = access_token_data.get('crawl_start_time')
        if lasttime:
            print 'last crawling finish time: %s' % lasttime
        lasttime = access_token_data.get('crawl_finish_time')
        if lasttime:
            print 'last crawling end time: %s' % lasttime
        print 'skip this user\n'        
        return

    print 'begin saving %s(%s) ...' % (access_token_data['uid'], uid)
    #print uid,access_token
    graph = GraphAPI(access_token)

    actions = ['me','feed','likes','notes','friends','friendlists','friendrequests','mutualfriends', \
               'birthday','tagged','activities','checkins','subscribedto','events', \
               'groups','movies','games','music','television','books','links', \
               'statuses','about','friendrequests','notifications',
              ]

    # record crawling start time
    crawl_start_time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())

    # do all crawling
    map(partial(save_one_user_graph_data, uid, graph, access_token_data.get('crawl_start_time')), actions)

    # save start and finished time
    #access_token_data['crawl_start_time'] = crawl_start_time_str
    #access_token_data['crawl_finish_time'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    # need_crawl is set to 1 only when the user visit fbreader site again
    #access_token_data['need_crawl'] = '0'

    #accessdb.update({'uid': uid}, access_token_data)
    #print access_token_data
    #time.sleep(1)
    #print 'done saving %s(%s)\n' % (access_token_data['name'], uid)


def main():
    token={}
    score=sys.argv[3]
    token['uid']=sys.argv[1]
    token['access_token']=sys.argv[2]
    token['need_crawl']=u'1'
    token['crawl_finish_time']=u'2014-01-08T14:14:13'
    token['crawl_start_time']=u'2014-01-08T14:13:48'
    #token['added_time']=u'2014-01-08T14:12:18'
    save_score(token['uid'],score)
    save_one_user(token)
    exit()



if __name__=="__main__":
    #print 1
    main()


