from selenium import webdriver
import time


from db_calls.crud import get_all_ids, update_furnace


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

if __name__ == "__main__":
    gift = "847dPBVex"
    gift_code(gift)