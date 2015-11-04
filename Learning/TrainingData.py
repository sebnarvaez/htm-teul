#!python2
#-*- coding: utf-8 -*-
#  TrainingData.py
#  Autor: Larvasapiens <sebasnr95@gmail.com>
#  Fecha creación: 2015-11-02
#  Fecha última modificación: 2015-11-02
#  Versión: 1.0 [estable]

trainingData = (
    (('mover', 'hacia', 'la', 'derecha'),                            ('action-mover', 'action-derecha')),
    (('mover', 'a', 'la', 'derecha'),                                ('action-mover', 'action-derecha')),
    (('mover', 'para', 'la', 'derecha'),                             ('action-mover', 'action-derecha')),
    (('por', 'favor', 'mover', 'a', 'la', 'derecha'),                ('action-mover', 'action-derecha')),
    (('quiero', 'mover', 'hacia', 'la', 'derecha'),                  ('action-mover', 'action-derecha')),
    (('moverse', 'para', 'la', 'derecha'),                           ('action-mover', 'action-derecha')),
    (('¿', 'podrias', 'moverlo', 'hacia', 'la', 'derecha', '?'),     ('action-mover', 'action-derecha')),
    ###
    (('mover', 'hacia', 'la', 'izquierda'),                          ('action-mover', 'action-izquierda')),
    (('mover', 'a', 'la', 'izquierda'),                              ('action-mover', 'action-izquierda')),
    (('mover', 'para', 'la', 'izquierda'),                           ('action-mover', 'action-izquierda')),
    (('por', 'favor', 'mover', 'a', 'la', 'izquierda'),              ('action-mover', 'action-izquierda')),
    (('quiero', 'mover', 'hacia', 'la', 'izquierda'),                ('action-mover', 'action-izquierda')),
    (('moverse', 'para', 'la', 'izquierda'),                         ('action-mover', 'action-izquierda')),
    (('¿', 'podrias', 'moverlo', 'hacia', 'la', 'izquierda', '?'),   ('action-mover', 'action-izquierda')),
    ###
    (('mover', 'hacia', 'arriba'),                                   ('action-mover', 'action-arriba')),
    (('mover', 'a', 'arriba'),                                       ('action-mover', 'action-arriba')),
    (('mover', 'para', 'arriba'),                                    ('action-mover', 'action-arriba')),
    (('por', 'favor', 'mover', 'arriba'),                            ('action-mover', 'action-arriba')),
    (('quiero', 'mover', 'hacia', 'arriba'),                         ('action-mover', 'action-arriba')),
    (('moverse', 'para', 'arriba'),                                  ('action-mover', 'action-arriba')),
    (('¿', 'podrias', 'moverlo', 'hacia', 'arriba', '?'),            ('action-mover', 'action-arriba')),
    ###
    (('mover', 'hacia', 'abajo'),                                    ('action-mover', 'action-abajo')),
    (('mover', 'a', 'abajo'),                                        ('action-mover', 'action-abajo')),
    (('mover', 'para', 'abajo'),                                     ('action-mover', 'action-abajo')),
    (('por', 'favor', 'mover', 'abajo'),                             ('action-mover', 'action-abajo')),
    (('quiero', 'mover', 'hacia', 'abajo'),                          ('action-mover', 'action-abajo')),
    (('moverse', 'para', 'abajo'),                                   ('action-mover', 'action-abajo')),
    (('¿', 'podrias', 'moverlo', 'hacia', 'abajo, ?'),               ('action-mover', 'action-abajo')),
    ###
    (('hacia', 'la', 'derecha'),                                     ('action-nothing', 'action-nothing')),
    (('a', 'la', 'derecha'),                                         ('action-nothing', 'action-nothing')),
    (('para', 'la', 'derecha'),                                      ('action-nothing', 'action-nothing')),
    (('por', 'favor', 'a', 'la', 'derecha'),                         ('action-nothing', 'action-nothing')),
    (('quiero', 'hacia', 'la', 'derecha'),                           ('action-nothing', 'action-nothing')),
    (('para', 'la', 'derecha'),                                      ('action-nothing', 'action-nothing')),
    (('¿', 'podrias', 'hacia', 'la', 'derecha', '?'),                ('action-nothing', 'action-nothing'))
)
    
#actionsData = (
    #('action-mover', 'action-derecha'),
    #('action-mover', 'action-derecha'),
    #('action-mover', 'action-derecha'),
    #('action-mover', 'action-derecha'),
    #('action-mover', 'action-derecha'),
    #('action-mover', 'action-derecha'),
    #('action-mover', 'action-derecha'),
    ####
    #('action-mover', 'action-izquierda'),
    #('action-mover', 'action-izquierda'),
    #('action-mover', 'action-izquierda'),
    #('action-mover', 'action-izquierda'),
    #('action-mover', 'action-izquierda'),
    #('action-mover', 'action-izquierda'),
    #('action-mover', 'action-izquierda'),
    ####
    #('action-mover', 'action-arriba'),
    #('action-mover', 'action-arriba'),
    #('action-mover', 'action-arriba'),
    #('action-mover', 'action-arriba'),
    #('action-mover', 'action-arriba'),
    #('action-mover', 'action-arriba'),
    #('action-mover', 'action-arriba'),
    ####
    #('action-mover', 'action-abajo'),
    #('action-mover', 'action-abajo'),
    #('action-mover', 'action-abajo'),
    #('action-mover', 'action-abajo'),
    #('action-mover', 'action-abajo'),
    #('action-mover', 'action-abajo'),
    #('action-mover', 'action-abajo'),
    ####
    
    #('action-derecha', 'action-nothing'),
    #('action-derecha', 'action-nothing'),
    #('action-derecha', 'action-nothing'),
    #('action-derecha', 'action-nothing'),
    #('action-derecha', 'action-nothing'),
    #('action-derecha', 'action-nothing'),
#)
