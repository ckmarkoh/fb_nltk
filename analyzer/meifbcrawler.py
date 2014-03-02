from functools import partial
from facebook import FacebookAPI, GraphAPI
import facebook
#import meifbreader
from pprint import pprint
import time
#from access_token_queue import AccessTokenQueue
import json
import sys
import re


crawl_all = True

def get_paging_parameters(url):
    actionparams_list = re.findall(r'\w+=\w+', url)
    actionparams = {}     
    for p in actionparams_list:
        ent = p.split('=')
        if ent[0] != 'access_token':
            actionparams[ent[0]] = ent[1]

    return actionparams

def save_one_user_graph_data(uid, graph, last_start_time_str, action): 
    #print ' action = ' + action

    # convert string to struct_time
    # original format '2012-11-24T17:18:44'
    fw=open("./subjects/users.u%s.%s.json"%(uid,action),'w')
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
            print grapherr
            fw.write('\n'.join(fwlist))
            fw.close()
            return

        # if action is just me, add the whole result directly
        if target_to_get == 'me':
            #user.me.update({time_field_to_check : graph_result[time_field_to_check]}, graph_result, upsert = True)
            #print graph_result #savesave
            fwlist.append(json.dumps(graph_result))
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
            item_saved_count += 1

        print '  %d items saved' % item_saved_count

        # determine if next round needed
        if not crawl_all or not graph_paging_next_params or got_old_post:
            break
        print '  next round:', graph_paging_next_params

    #print ' done saving action "%s", all %d item(s)\n' % (action, user[action].count())
    fw.write('\n'.join(fwlist))
    fw.close()
    print ' done saving action "%s"' % (action)


def save_one_user(access_token_data):
    access_token = access_token_data['access_token']
    uid = access_token_data['uid']
    #user = users['u%s' % uid]
     
    #print uid
   
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
    access_token_data['crawl_start_time'] = crawl_start_time_str
    access_token_data['crawl_finish_time'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
    # need_crawl is set to 1 only when the user visit fbreader site again
    access_token_data['need_crawl'] = '0'

    #accessdb.update({'uid': uid}, access_token_data)
    #print access_token_data

    time.sleep(2)
    #print 'done saving %s(%s)\n' % (access_token_data['name'], uid)


# save all users' data

#print 'Current acccess_token count = %d\n' % accessdb.count()
#print 'Just [ENTER] to start crawling, other input to exit'
#if raw_input():
#    exit()
#access_queue = AccessTokenQueue(accessdb)
#for token in access_queue:
#    print 'Now processing %d/%d:' % (access_queue.get_cur_pos(), len(access_queue))
#    #pprint(token)
#
#    print "token",token
#    print
#    save_one_user(token)
#    print
#    time.sleep(2)
token={}
#token['uid']=u'1037998582'
#token['access_token']=u'CAAFbxFk1h5QBANvdl6NYxcAZCQxCGKh6WPWQZCVz3ZC0POjW3HZBE0u8WFMVMSPbIbDpxtwPnop3A8KDArhjhukd1D9c0fo8vh32YahXaieBYDkfnw2w2h3YBnACUZAlO507TUaqz5VpjaKQVOLAllziRr9NfdFZCGE82EXKnBy61k4G4avxny'
#token['name']=u'Emily Lu'
token['uid']=sys.argv[1]
token['access_token']=sys.argv[2]
token['need_crawl']=u'1'
token['crawl_finish_time']=u'2014-01-08T14:14:13'
token['crawl_start_time']=u'2014-01-08T14:13:48'
token['known_code']=u'ca5a5d8a2e17bcab374316b463a697f804e5be64'
token['added_time']=u'2014-01-08T14:12:18'
#token=json.loads(u'{"uid":"1037998582"}')

#print "token",token
save_one_user(token)

exit()



