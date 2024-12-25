def draw_instructions(screen, font):
    instructions = [
        "Use arrow keys or WASD to move.",
        "Press right-click to shoot.",
        "Press any key to start.",
        "Try not to get caught by snowmans",
        "Good luck!"
    ]
    white = (255, 255, 255)
    for i, line in enumerate(instructions):
        text_surface = font.render(line, True, white)
        screen.blit(text_surface, (20, 20 + i * 40))