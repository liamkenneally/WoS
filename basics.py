from selenium import webdriver
import time

from db_calls.crud import add_user, get_all_ids, update_furnace

################################################ BULK REGISTER ####################################################################

# Bulk register will take a list of game IDs and add them to the database 
def bulk_register():
    #GoT_user_list = [110826180,108871167,105364765,105987437,106036691,107871829,107347154,108494023,107511021,106151242,105741734,107298065,118153053,106905217,106036959,108510859,105692676,105512485,106822802,105168400,107544132,109035137,105233605,105839825,108576307,107511201,106528418,107249082,106167744,107069030,105020967,108265069,106053385,107494947,106675609,105676505,105987789,107707682,105086294,116457670,105626941,106167503,105692653,106331615,108723815,105217833,105791025,104988053,107675267,109838838,105004577,106839512,104906427,106019986,104922382,108035625,105119376,106036570,105529057,107085427,106003666,108281133,107675048,106396851,106200280,108084845,108248713,107904627,106806795,113616304,108297825,108330209,105757863,106725076,108051636,108477777,112153334,108674566,108723641,106511770,105168112,108707562,105938432,108527153,105102560,115846344,108854981,105414155,104889557,105627375,106757710,107986125,106266080,106069545,107232604,106003952,105168379]
    #RiM_user_list = [108871167,105021002,108134128,108281396,105839825,105365136,106167744,105955071,105184832,105249968,107806089,106577269,110933946,107347410,107085427,107478548,105479716,106102464,107674849,105152196,108084654,105643207,108134090,107150893,107118223,105725590,106200215,108657886,105807539,106921481,106905194,105250186,106757419,107822779,105709305,108510555,108871406,108969123,105168073,106954431,108231942,108199378,105922264,106397049,116755028,108363153,106790081,114697964,105971279,105544985,107658586,108559828,107544026,106347989,107281840,107396677,107888356,108936948,106610316,106298939,105233851,108264806,106839568,107969815,106642779,107756744,107887774,108035832,107380335,106413736,107150765,105561376,109018635,108297710,108379528,106905121,107691406,106085904,109018478,106921178,108019367,108019348,107019467,108477789,106986657,106380520,105709109,107592905,105905784,107068999,108379539,112695994,108117199,126987347,105414131,105135340,105725131,122440652]
    # misc_users = [106904909,104971875,105217694,106708654,105315689,107036259,108772920,108134024]
    # misc_users = [110826180,108871167,109925135,105364765,106036691,107626231,105987437,107216881,108494023,104873689,107871829,108510859,107298065,108445289,106905217,106053385,112900352,107511021,105839825,106036959,107511201,105692676,106528418,105594056,105168400,106430070,109035137,105626941,107544132,106462777,105512485,108265069,105823580,108576307,125782313,105987789,105020967,115846344,108674491,107707682,107249082,108068108,105233605,107511251,108150354,106839512,105774774,105692653,108772920,106053192,106396851,112972893,106675609,109838838,108936399,106019986,105676505,108018941,105791025,108134024,107494947,104922382,107675267,106331615,108035625,106020457,112153334,105955063,104906427,108707377,108723815,105086294,106216843,107740597,104988053,106052907,106757388,107675048,108084845,107036024,108510637,116457670,106200280,105987407,115293582,107691443,108903624,106725076,106478762,104889557,106102374,105070321,108592439,108723878,105217694,106904909,105757863,106511770,105168156]
    misc_users = []
    
    for user in misc_users:
        get_userInfo(user)

def get_userInfo(userID): 
    options = webdriver.ChromeOptions()
    web = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=options)
    
    web.get("https://wos-giftcode.centurygame.com/")
    user_field = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[1]/input")
    user_field.send_keys(userID)
    web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[2]").click()
    time.sleep(1)
    
    
    user = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/p[1]").text
    try:
        furnace = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/p[2]/img").get_attribute("src")
        furnace = furnace[-5:]
        furnace = furnace[:1]
        furnace = {
            "1": "FC1", 
            "2": "FC2", 
            "3": "FC3",
            "4": "FC4", 
            "5": "FC5",
            "6": "FC6"
        }.get(furnace)
    except:
        furnace = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/p[2]").text
        furnace = int(furnace[14:])
    state = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/p[3]").text
    state = int(state[6:])
    web.quit()
    return add_user(userID, user, furnace, state)
################################################ BULK REGISTER ####################################################################


################################################ GIFT CODE ####################################################################
def gift_code(lowered):
    userIDs = get_all_ids()
    user_info = []
    server_busy = []
    
    for userID in userIDs:
        options = webdriver.ChromeOptions()
        web = webdriver.Remote(command_executor="http://127.0.0.1:4444", options=options)
        #web = webdriver.Remote(command_executor="http://selenium-hub:4444", options=options)
        #web = webdriver.Chrome()
        web.get("https://wos-giftcode.centurygame.com/")
        gift_code = lowered
        user_field = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[1]/input")
        gift_code_field = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[2]/div[1]/input")
        user_field.send_keys(userID)
        gift_code_field.send_keys(gift_code)
        # Select user 
        time.sleep(1)
        web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/div[2]").click()
        time.sleep(1)
                #### Code to update users Furnace levels when a new giftcode is claimed
        try:
            furnace = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/p[2]/img").get_attribute("src")
            furnace = furnace[-5:]
            furnace = furnace[:1]
            furnace = {
                "1": "FC1", 
                "2": "FC2", 
                "3": "FC3",
                "4": "FC4", 
                "5": "FC5",
                "6": "FC6"
            }.get(furnace)
        except:
            furnace = web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[1]/div[1]/p[2]").text
            furnace = int(furnace[14:])
        #submit user
        web.find_element("xpath", "/html/body/div/div/div/div[3]/div[2]/div[3]").click()

        #submission message
        time.sleep(1)
        text = web.find_element("xpath", "/html/body/div/div/div[2]/div[2]/p").text
        if "server busy" in text.lower():
            server_busy.append(f'{userID} {text}')
        else:
            user_info.append(f'{userID}, {text}')
        web.quit()
        #Test
        update_furnace(userID, furnace)
        print(user_info, server_busy)
    return user_info
################################################ GIFT CODE ####################################################################


if __name__ == "__main__":
# Uncomment this to bulk register users
#    bulk_register()
    
# when scipt is executed gets all users from DB and applys the giftcode one by one to each user
    gift = "DC780k"
    gift_code(gift)