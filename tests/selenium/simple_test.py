# tests/selenium/simple_test.py
from selenium import webdriver
import time

def test_click_buttons():
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://nutritrack.ru/diet")
        time.sleep(2)
        
        buttons = driver.find_elements("tag name", "button")
        print(f"Найдено кнопок: {len(buttons)}")
        
        for i, button in enumerate(buttons):
            try:
                # Прокручиваем к кнопке перед кликом
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(0.2)
                
                if button.is_displayed() and button.is_enabled():
                    print(f"Кликаем кнопку {i}: {button.text}")
                    button.click()
                    time.sleep(0.5)
                    
                    # Пробуем найти и нажать "Отмена" или "Готово"
                    try:
                        close_buttons = driver.find_elements("tag name", "button")
                        for close_btn in close_buttons:
                            if close_btn.text in ["Отмена", "Готово"]:
                                print(f"Нашли кнопку '{close_btn.text}', нажимаем!")
                                close_btn.click()
                                time.sleep(0.5)
                                break
                    except:
                        pass
                        
            except:
                print(f"Не удалось кликнуть кнопку {i}")
                continue
                
        print("Все кнопки протестированы!")
        
    finally:
        driver.quit()

def test_click_links():
    driver = webdriver.Chrome()
    
    try:
        driver.get("https://nutritrack.ru/diet")
        time.sleep(2)
        
        links = driver.find_elements("tag name", "a")
        print(f"Найдено ссылок: {len(links)}")
        
        for i, link in enumerate(links[:3]):
            try:
                # Прокручиваем к ссылке перед кликом
                driver.execute_script("arguments[0].scrollIntoView();", link)
                time.sleep(0.2)
                
                if link.is_displayed() and link.is_enabled():
                    print(f"Кликаем ссылку {i}: {link.text}")
                    link.click()
                    time.sleep(1)
                    driver.back()  # Возвращаемся назад
                    time.sleep(1)
            except:
                print(f"Не удалось кликнуть ссылку {i}")
                continue
                
        print("Все ссылки протестированы!")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_click_buttons()
    test_click_links()