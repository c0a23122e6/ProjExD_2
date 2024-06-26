import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, 5),
         pg.K_LEFT: (-5, 0), 
         pg.K_RIGHT: (5, 0)}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """こうかとんRect、または爆弾Rectの画面内外判定用の関数
    引数:こうかとんRect,または爆弾Rect
    戻り値：横方向判定結果、縦方向判定結果（True:画面内/False:画面外）"""
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate        


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    clock = pg.time.Clock()
    tmr = 0
    vx = +5
    vy = +5
    font = pg.font.Font(None, 200)
    txt = font.render(str("Game Over"), True, (255, 255, 255))
    # Game Overを表示
    black = pg.Surface((WIDTH, HEIGHT))
    black.set_alpha(200)
    # 黒背景を透過
    ck_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 4.0)# 泣いてるこうかとん参照
    ck_rct = ck_img.get_rect()
    ck_rct.center = 900, 400

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            # 工科とんと爆弾がぶつかったらゲームオーバー
            screen.blit(bg_img, [0, 0])
            screen.blit(black, [0, 0])
            screen.blit(ck_img, ck_rct)
            screen.blit(txt, [500, 200])
            pg.display.update()
            # 画面を更新
            clock.tick(1/5)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
