def wrap_text(text, max_length=36):
    """
    Разбивает текст на строки по пробелам, чтобы каждая строка была не длиннее max_length.
    Возвращает список строк.
    """
    if len(text) <= max_length:
        return [text]
    
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        # Проверяем, поместится ли слово в текущую строку
        test_line = ' '.join(current_line + [word])
        if len(test_line) <= max_length:
            current_line.append(word)
        else:
            # Если текущая строка не пустая, сохраняем её
            if current_line:
                lines.append(' '.join(current_line))
            # Начинаем новую строку с текущим словом
            current_line = [word]
    
    # Добавляем последнюю строку
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines