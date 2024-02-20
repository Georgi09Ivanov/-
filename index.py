import random
import pygame
import sys
import io

# Променяме стандартната кодировка на конзолата на UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8")

# Проверка за правописни грешки
def провери_правопис(word, correct_word):
    return word == correct_word

# Главна функция
def main():
    # Създаване на прозорец с размери 800x600
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Правописна игра")

    # Цвят на фона и шрифт
    background = (255, 255, 255)
    font = pygame.font.Font(None, 36)

    # Списък с правилно написаните думи
    правилни_думи = [
        "абонамент", "актуален", "аперитив", "артериален", "аудио-визуален", 
        "бенка", "бомбардирам", "буквено-цифров", "вакуум", "възпирам", 
        "въплъщение", "въстание", "вдругиден", "виделина", 
        "военноисторически", "възравдане", 
    ]

    # Инициализация на списък с грешно написани думи и техните правилни варианти
    грешни_думи = {
    "абонамент": "абонамент", 
    "актуален": "актуален", 
    "аперетив": "аперитив", 
    "артериален": "артериален", 
    "аудио визоаленн": "аудио-визуален",
    "бенка": "бенка", 
    "бумбардирамм": "бомбардирам", 
    "буквеноцифров": "буквено-цифров",
    "вакум": "вакуум", 
    "вазпирам": "възпирам", 
    "въплъщенние": "въплъщение", 
    "въсттанние": "въстание", 
    "другиден": "вдругиден", 
    "виделена": "виделина",
    "военноизторически": "военноисторически", 
}

    # Генериране на грешно написани думи за всеки елемент от списъка с правилни думи
    for word in правилни_думи:
        грешен_вариант = word[::-1]  # Примерен метод за генериране на грешен вариант
        грешни_думи[грешен_вариант] = word

    # Променливи за точките и броя на оставащите думи
    точки = 0
    оставащи_думи = len(грешни_думи)

    # Списъци за правилно и грешно написаните думи
    правилно_написани = []
    грешно_написани = []

    # Главна игрова петъл
    running = True
    while running:
        screen.fill(background)
        
        # Избор на случайна грешно написана дума и нейния правилен вариант
        wrong_word, correct_word = random.choice(list(грешни_думи.items()))

        # Изобразяване на грешно написаната дума на екрана
        text = font.render(f"Препиши \"{wrong_word}\":", True, (0, 0, 0))
        screen.blit(text, (50, 50))

        # Изобразяване на броя на оставащите думи
        remaining_text = font.render(f"Остават: {оставащи_думи} думи", True, (0, 0, 0))
        screen.blit(remaining_text, (50, 10))

        # Отчитане на въведения от играча текст
        input_text = ""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Проверка за правилно преписване на думата
                        if провери_правопис(input_text, correct_word):
                            точки += 1
                            правилно_написани.append(correct_word)
                        else:
                            точки -= 1
                            грешно_написани.append((wrong_word, correct_word))
                        оставащи_думи -= 1
                        del грешни_думи[wrong_word]  # Премахване на използваната дума
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:  # Изход от играта с ESC
                        pygame.quit()
                        sys.exit()

                    else:
                        input_text += event.unicode

            # Изобразяване на въведения текст в текстово поле
            pygame.draw.rect(screen, (255, 255, 255), (50, 100, 700, 50))  # Изтриване на предишния текст
            input_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(input_surface, (50, 100))

            pygame.display.flip()

            # Проверка за въвеждане на правилния текст
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                break

        # Проверка за край на играта
        if оставащи_думи == 0:
            running = False

        pygame.display.flip()

    # Изход от играта
    pygame.quit()

    # Връщане на резултата и списъците с правилно и грешно написаните думи
    return точки, правилно_написани, грешно_написани

if __name__ == "__main__":
    точки, правилно_написани, грешно_написани = main()
    # Извеждане на резултата
    print(f"Точки: {точки}")

    # Запис на резултатите във файл
    with open("резултати.txt", "w", encoding="utf-8") as file:
        file.write(f"Точки: {точки}\n")
        file.write("Правилно написани думи:\n")
        for word in правилно_написани:
            file.write(f"[Правилно] {word}\n")
        file.write("Грешно написани думи:\n")
        for wrong_word, correct_word in грешно_написани:
            file.write(f"[Грешно] {wrong_word} ({correct_word})\n")

    print("Резултатите са записани във файл 'резултати.txt'")
