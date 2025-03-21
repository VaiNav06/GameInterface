import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

# Actions for RL Agent
ACTION_LEFT = 0
ACTION_RIGHT = 1
ACTION_FIRE = 2
ACTION_NOOP = 3  # No operation (do nothing)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        if sb:
            sb.prep_high_score()

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Check if aliens reach the bottom
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = (ai_settings.screen_width - 2 * alien.rect.width) // (2 * alien.rect.width)
    number_rows = (ai_settings.screen_height - (3 * alien.rect.height) - ship.rect.height) // (2 * alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)
            if sb:
                sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    stats.ships_left -= 1  

    if stats.ships_left > 0:  
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        pygame.time.delay(1000)
    else: 
        stats.ships_left = 0
        stats.game_active = False
        pygame.mouse.set_visible(True)
        
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    if sb:
        sb.prep_score()  
        sb.show_score()

    if not stats.game_active and play_button:
        play_button.draw_button()

    pygame.display.flip()  

    pygame.display.flip()

def show_game_over(screen, stats, sb):
    
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    final_score_text = font.render(f"Final Score: {stats.score}", True, (0, 0, 0))

    screen_rect = screen.get_rect()
    screen.blit(game_over_text, game_over_text.get_rect(center=(screen_rect.centerx, screen_rect.centery - 50)))
    screen.blit(final_score_text, final_score_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 20)))

    
    if sb:
        sb.prep_score()
        sb.show_score()

    
