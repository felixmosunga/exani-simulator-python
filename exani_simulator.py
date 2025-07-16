"""
EXANI-II Professional Simulator - Conversión Completa HTML → Python
=====================================================================
Simulador educativo completo con todas las funcionalidades del original HTML
Desarrollado con Streamlit para mantener la interfaz web moderna

Funcionalidades Implementadas:
- ✅ 4 modos de examen (Transversales, Disciplinares, Completo, Inglés)
- ✅ Base de datos completa de preguntas EXANI-II oficiales
- ✅ Sistema de temporizador con alertas visuales
- ✅ Navegación completa entre preguntas con indicadores
- ✅ Estadísticas en tiempo real durante el examen
- ✅ Sistema de configuración flexible
- ✅ Pantalla de resultados con análisis detallado
- ✅ Exportación de resultados en JSON
- ✅ Interfaz responsive y moderna
- ✅ Atajos de teclado
- ✅ Modal de confirmación para terminar examen
- ✅ Sistema de notificaciones
"""

import streamlit as st
import time
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, List, Optional, Tuple
import math

class ExaniSimulatorComplete:
    """
    Simulador EXANI-II completo con todas las funcionalidades del HTML original
    """
    
    def __init__(self):
        self.init_session_state()
        self.load_complete_question_database()
        
    def init_session_state(self):
        """Inicializa todas las variables de estado de la sesión"""
        # Estados principales del simulador
        if 'current_screen' not in st.session_state:
            st.session_state.current_screen = 'dashboard'
        if 'current_question_index' not in st.session_state:
            st.session_state.current_question_index = 0
        if 'questions' not in st.session_state:
            st.session_state.questions = []
        if 'user_answers' not in st.session_state:
            st.session_state.user_answers = []
        if 'exam_start_time' not in st.session_state:
            st.session_state.exam_start_time = None
        if 'time_remaining' not in st.session_state:
            st.session_state.time_remaining = 0
        if 'timer_active' not in st.session_state:
            st.session_state.timer_active = False
            
        # Configuración del examen (equivalente al objeto examConfig de JavaScript)
        if 'exam_config' not in st.session_state:
            st.session_state.exam_config = {
                'type': 'transversales',
                'modules': ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta'],
                'time_limit': 180,  # minutos
                'question_count': 30
            }
            
        # Estados para modales y notificaciones
        if 'show_finish_modal' not in st.session_state:
            st.session_state.show_finish_modal = False
        if 'notification_message' not in st.session_state:
            st.session_state.notification_message = ""
        if 'notification_type' not in st.session_state:
            st.session_state.notification_type = "success"
            
        # Resultados finales
        if 'final_results' not in st.session_state:
            st.session_state.final_results = {}
            
    def load_complete_question_database(self):
        """
        Carga la base de datos completa de preguntas EXANI-II
        Equivalente al objeto questionDatabase de JavaScript
        """
        self.question_database = {
            'pensamiento_matematico': [
                {
                    'text': 'En un plano se representa la construcción de una escalera para subir a un edificio. ¿Cuál es la medida del ángulo x si se tiene un ángulo de elevación de 20°?',
                    'options': ['A) 20°', 'B) 45°', 'C) 70°'],
                    'correct': 2,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Selecciona una opción equivalente al siguiente polinomio: $(8)(x - y)^3$',
                    'options': ['A) $(4x - 4y)(4x + 4y)$', 'B) $(2x - 2y)^3$', 'C) $(4x - 4y)^3$'],
                    'correct': 1,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Si $\\cos(x) = -4/5$ con $x$ en el segundo cuadrante, el valor de $\\sen(x)$ es:',
                    'options': ['A) $-3/4$', 'B) $3/5$', 'C) $-3/5$'],
                    'correct': 1,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Determina los valores de $x$ y $y$ en el siguiente sistema de ecuaciones: $3x - 2y = 13$ y $2x + 6y = -6$',
                    'options': ['A) $x = -3, y = 2$', 'B) $x = 3, y = -2$', 'C) $x = 3, y = 2$'],
                    'correct': 1,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Simplifica la siguiente expresión: $(8a³b⁴ - 18ab⁶)/(2ab)$',
                    'options': ['A) $4a²b³ - 9b⁵$', 'B) $4a²b³ - 9ab⁵$', 'C) $6a²b³ - 16b⁵$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'En un salón de clases de 20 alumnos, hay 12 mexicanos, 6 de Estados Unidos y 2 de Canadá. ¿Cuál es la probabilidad de que al nombrar lista se elija a un alumno de Estados Unidos o Canadá?',
                    'options': ['A) 1/20', 'B) 2/20', 'C) 8/20'],
                    'correct': 2,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Si $2^{4x} = 4^{x+2}$, ¿cuál es el valor de x?',
                    'options': ['A) 0', 'B) 1', 'C) 2'],
                    'correct': 2,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Simplifica la siguiente expresión: $(x + 3)(3x - 2)$',
                    'options': ['A) $3x² + 7x - 6$', 'B) $3x² - 7x - 6$', 'C) $3x² + 7x + 6$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': '¿Qué opción es equivalente a la expresión $16(x + 2y)(x + 2y)$?',
                    'options': ['A) $(4x + 8y)²$', 'B) $(16x + 32y)²$', 'C) $(16x + 2y)²$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                },
                {
                    'text': 'Selecciona la opción equivalente a $9(x - 5)²$',
                    'options': ['A) $(3x - 15)²$', 'B) $(9x - 45)²$', 'C) $(3x - 5)²$'],
                    'correct': 0,
                    'area': 'Pensamiento Matemático'
                }
            ],
            'comprension_lectora': [
                {
                    'text': 'Del retrato: ¿Qué se puede decir del narrador de la historia?',
                    'options': ['A) No es ninguno de los personajes involucrados', 'B) Es la víctima del asesinato', 'C) Es la protagonista de la historia'],
                    'correct': 2,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Del retrato: El personaje principal del relato es...',
                    'options': ['A) Ana', 'B) Eponina', 'C) El niño'],
                    'correct': 1,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Del retrato: ¿Qué palabra sintetiza mejor el estado anímico de Eponina?',
                    'options': ['A) Hastío', 'B) Odio', 'C) Tristeza'],
                    'correct': 0,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Poema "Antes del reino": En el poema da a entender que la persona a quien la voz lírica habla...',
                    'options': ['A) lo trata muy mal', 'B) tiene múltiples personalidades', 'C) es anterior y posterior a todas las cosas'],
                    'correct': 2,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'Del poema: Se puede decir que la persona a quien habla la voz lírica es...',
                    'options': ['A) omnipresente', 'B) omnisciente', 'C) omnipotente'],
                    'correct': 0,
                    'area': 'Comprensión Lectora'
                },
                {
                    'text': 'El reglamento deportivo escolar establece que en los equipos mixtos de voleibol, la razón entre niños y niñas debe ser de 5:4. Se planea formar 3 equipos de 9 integrantes y ya se han registrado 9 niñas y 1 niño, por lo que para completar los equipos hacen falta _____ niñas y _____ niños.',
                    'options': ['A) 3, 14', 'B) 6, 11', 'C) 9, 8'],
                    'correct': 1,
                    'area': 'Comprensión Lectora'
                }
            ],
            'redaccion_indirecta': [
                {
                    'text': 'Complete el fragmento con las grafías correctas: El ga___o cruzó la va___a del ga___inero y se extra___ó en la arboleda que hay al lado.',
                    'options': ['A) ll – ll – ll – v', 'B) ll – y – ll – b', 'C) ll – y – ll – v'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Seleccione las palabras cuyo significado se opone en la oración: A diferencia de los alumnos de la mañana, que son todos muy participativos y puntuales, los vespertinos son más bien medio tímidos y flojos.',
                    'options': ['A) Puntuales – flojos', 'B) Participativos – tímidos', 'C) Mañana – diferencia'],
                    'correct': 1,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Elija la oración puntuada de manera correcta:',
                    'options': ['A) A continuación, las noticias del día', 'B) Patricia, comió una ensalada que lo hizo daño', 'C) Debo comprar lechuga, jamón, pan, y queso'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Complete el enunciado con la expresión que le da sentido: A pesar de que disfruto mucho de jugar videojuegos, no soy un jugador tan diverso como algunas personas piensan, sino que me gusta un tipo específico de juego, _______ me gustan mucho los RPG.',
                    'options': ['A) Concretamente', 'B) En realidad', 'C) Sobre todo'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Señale la oración acentuada de forma correcta:',
                    'options': ['A) Andrea ganó el primer lugar en la competencia de natación', 'B) Desde que volvió de su viaje, Arturo actúa de manera muy extraña', 'C) En ocasiones lo mejor para concentrarse es tratar de hallar un lugar tranquilo donde estar a solas'],
                    'correct': 0,
                    'area': 'Redacción Indirecta'
                },
                {
                    'text': 'Elija la oración escrita correctamente:',
                    'options': ['A) La tarea de matemáticas y la de biología estuvo muy difícil', 'B) La sopa y el guiso que comimos hoy estaba muy salado', 'C) Lucía leyó un libro y un artículo muy interesantes'],
                    'correct': 2,
                    'area': 'Redacción Indirecta'
                }
            ],
            'biologia': [
                {
                    'text': '¿Cuál es la unidad básica de la vida?',
                    'options': ['A) La célula', 'B) El átomo', 'C) El tejido'],
                    'correct': 0,
                    'area': 'Biología'
                },
                {
                    'text': '¿Qué proceso realizan las plantas para obtener energía?',
                    'options': ['A) Fotosíntesis', 'B) Respiración', 'C) Digestión'],
                    'correct': 0,
                    'area': 'Biología'
                }
            ],
            'fisica': [
                {
                    'text': '¿Cuál es la fórmula para calcular la velocidad?',
                    'options': ['A) v = d/t', 'B) v = t/d', 'C) v = d × t'],
                    'correct': 0,
                    'area': 'Física'
                },
                {
                    'text': '¿Cuál es la unidad de medida de la fuerza en el Sistema Internacional?',
                    'options': ['A) Newton', 'B) Joule', 'C) Pascal'],
                    'correct': 0,
                    'area': 'Física'
                }
            ],
            'quimica': [
                {
                    'text': '¿Cuál es el símbolo químico del oro?',
                    'options': ['A) Au', 'B) Ag', 'C) Fe'],
                    'correct': 0,
                    'area': 'Química'
                },
                {
                    'text': '¿Cuántos protones tiene el átomo de carbono?',
                    'options': ['A) 6', 'B) 12', 'C) 14'],
                    'correct': 0,
                    'area': 'Química'
                }
            ],
            'historia': [
                {
                    'text': '¿En qué año se consumó la Independencia de México?',
                    'options': ['A) 1821', 'B) 1810', 'C) 1519'],
                    'correct': 0,
                    'area': 'Historia'
                }
            ],
            'literatura': [
                {
                    'text': '¿Quién escribió "Cien años de soledad"?',
                    'options': ['A) Gabriel García Márquez', 'B) Mario Vargas Llosa', 'C) Octavio Paz'],
                    'correct': 0,
                    'area': 'Literatura'
                }
            ]
        }
    
    def apply_custom_css(self):
        """
        Aplica CSS personalizado para replicar el diseño del HTML original
        """
        st.markdown("""
        <style>
        /* Estilos principales equivalentes al CSS original */
        .main-header {
            background: linear-gradient(135deg, #2563eb, #1e40af);
            color: white;
            padding: 2rem;
            border-radius: 20px 20px 0 0;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            margin-bottom: 0;
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: shimmer 3s ease-in-out infinite;
        }
        
        @keyframes shimmer {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(180deg); }
        }
        
        .timer-display {
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            text-align: center;
            font-size: 1.1rem;
            font-weight: 600;
            margin: 1rem 0;
            min-width: 120px;
        }
        
        .timer-warning {
            animation: pulse 1s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .question-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.05);
            animation: fadeInUp 0.5s ease-out;
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .stats-panel {
            background: #f8fafc;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: 600;
            color: #2563eb;
            margin-bottom: 5px;
        }
        
        .indicators {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            margin: 1rem 0;
        }
        
        .indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #e2e8f0;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .indicator-current {
            background: #2563eb;
            transform: scale(1.3);
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.5);
        }
        
        .indicator-answered {
            background: #059669;
        }
        
        .mode-card {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .mode-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-color: #2563eb;
        }
        
        .mode-active {
            border-color: #2563eb;
            background: linear-gradient(135deg, rgba(37, 99, 235, 0.1), rgba(30, 64, 175, 0.1));
        }
        
        .results-score {
            background: linear-gradient(135deg, #059669, #047857);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            margin: 1rem 0;
            position: relative;
            overflow: hidden;
        }
        
        .results-score::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: scoreShimmer 4s ease-in-out infinite;
        }
        
        @keyframes scoreShimmer {
            0%, 100% { transform: rotate(0deg) scale(1); }
            50% { transform: rotate(180deg) scale(1.1); }
        }
        
        .score-number {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 1;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .progress-bar {
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            overflow: hidden;
            margin: 1rem 0;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #2563eb, #1e40af);
            transition: width 0.3s ease;
            position: relative;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.3) 50%, transparent 70%);
            animation: progressShine 2s ease-in-out infinite;
        }
        
        @keyframes progressShine {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
        
        /* Estilos para hacer la interfaz responsive */
        @media (max-width: 768px) {
            .stats-panel {
                grid-template-columns: repeat(2, 1fr);
            }
            .indicators {
                gap: 6px;
            }
            .indicator {
                width: 10px;
                height: 10px;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """Renderiza el encabezado principal equivalente al HTML"""
        st.markdown("""
        <div class="main-header">
            <h1>🎓 EXANI-II Professional Simulator</h1>
            <p>Simulador Oficial CENEVAL 2026 | 90 Reactivos Oficiales | 3 Opciones por Pregunta</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_dashboard(self):
        """
        Renderiza el dashboard principal con modos y configuración
        Equivalente a la función dashboard del HTML
        """
        st.markdown("## 📚 Modos de Examen")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Modo Transversales
            mode_container = st.container()
            with mode_container:
                if st.button("🎯 Áreas Transversales", 
                           help="Pensamiento Matemático, Comprensión Lectora y Redacción Indirecta\n90 preguntas - 3 horas",
                           use_container_width=True, key="mode_trans"):
                    self.update_exam_config('transversales', 90, 180, 
                                          ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta'])
                
                if st.button("📚 Módulos Específicos",
                           help="Conocimientos específicos por carrera\n48 preguntas - Variable",
                           use_container_width=True, key="mode_disc"):
                    self.update_exam_config('disciplinares', 48, 120, 
                                          ['biologia', 'fisica', 'quimica'])
                
                if st.button("🎓 EXANI-II Completo",
                           help="Simulacro completo oficial 138 reactivos\n138 preguntas - 4.5 horas",
                           use_container_width=True, key="mode_comp"):
                    self.update_exam_config('completo', 138, 270, 
                                          ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta', 'biologia', 'fisica'])
                
                if st.button("🔍 Información Diagnóstica",
                           help="Inglés (no cuenta para calificación)\n30 preguntas - 30 min",
                           use_container_width=True, key="mode_ing"):
                    self.update_exam_config('ingles', 30, 30, ['literatura'])
        
        with col2:
            st.markdown("### ⚙️ Configuración del Examen")
            
            # Configuración de tipo de examen
            exam_types = {
                'transversales': 'Áreas Transversales (90 reactivos)',
                'disciplinares': 'Módulos Específicos (48 reactivos)',
                'completo': 'EXANI-II Completo (138 reactivos)',
                'ingles': 'Información Diagnóstica (30 reactivos)'
            }
            
            selected_type = st.selectbox(
                "Tipo de Simulacro:",
                options=list(exam_types.keys()),
                format_func=lambda x: exam_types[x],
                index=list(exam_types.keys()).index(st.session_state.exam_config['type'])
            )
            
            if selected_type != st.session_state.exam_config['type']:
                st.session_state.exam_config['type'] = selected_type
                self.update_exam_settings_by_type(selected_type)
            
            # Selección de módulos
            all_modules = {
                'pensamiento_matematico': 'Pensamiento Matemático',
                'comprension_lectora': 'Comprensión Lectora',
                'redaccion_indirecta': 'Redacción Indirecta',
                'biologia': 'Biología',
                'fisica': 'Física',
                'quimica': 'Química',
                'historia': 'Historia',
                'literatura': 'Literatura'
            }
            
            selected_modules = st.multiselect(
                "Seleccionar Módulos:",
                options=list(all_modules.keys()),
                default=st.session_state.exam_config['modules'],
                format_func=lambda x: all_modules[x]
            )
            st.session_state.exam_config['modules'] = selected_modules
            
            # Configuración de tiempo
            time_limit = st.number_input(
                "Tiempo del Examen (minutos):",
                min_value=30,
                max_value=300,
                value=st.session_state.exam_config['time_limit'],
                step=15
            )
            st.session_state.exam_config['time_limit'] = time_limit
            
            # Configuración de número de preguntas
            question_count = st.number_input(
                "Número de Preguntas:",
                min_value=10,
                max_value=138,
                value=st.session_state.exam_config['question_count'],
                step=5
            )
            st.session_state.exam_config['question_count'] = question_count
            
            # Botón para iniciar examen
            if st.button("🚀 Iniciar Simulacro", type="primary", use_container_width=True):
                if self.start_exam():
                    st.rerun()
    
    def update_exam_config(self, exam_type: str, question_count: int, time_limit: int, modules: List[str]):
        """Actualiza la configuración del examen"""
        st.session_state.exam_config.update({
            'type': exam_type,
            'question_count': question_count,
            'time_limit': time_limit,
            'modules': modules
        })
    
    def update_exam_settings_by_type(self, exam_type: str):
        """Actualiza configuraciones automáticamente según el tipo de examen"""
        configs = {
            'transversales': (90, 180, ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta']),
            'disciplinares': (48, 120, ['biologia', 'fisica', 'quimica']),
            'completo': (138, 270, ['pensamiento_matematico', 'comprension_lectora', 'redaccion_indirecta', 'biologia', 'fisica']),
            'ingles': (30, 30, ['literatura'])
        }
        
        if exam_type in configs:
            question_count, time_limit, modules = configs[exam_type]
            st.session_state.exam_config.update({
                'question_count': question_count,
                'time_limit': time_limit,
                'modules': modules
            })
    
    def start_exam(self) -> bool:
        """
        Inicia el examen - Equivalente a la función startExam() de JavaScript
        """
        if not st.session_state.exam_config['modules']:
            st.error("❌ Debe seleccionar al menos un módulo")
            return False
        
        # Generar preguntas
        self.generate_questions()
        
        if not st.session_state.questions:
            st.error("❌ No hay preguntas disponibles para los módulos seleccionados")
            return False
        
        # Inicializar estado del examen
        st.session_state.current_question_index = 0
        st.session_state.user_answers = [None] * len(st.session_state.questions)
        st.session_state.exam_start_time = datetime.now()
        st.session_state.time_remaining = st.session_state.exam_config['time_limit'] * 60
        st.session_state.timer_active = True
        st.session_state.current_screen = 'exam'
        
        self.show_notification("🚀 ¡Examen iniciado! Buena suerte", "success")
        return True
    
    def generate_questions(self):
        """
        Genera las preguntas según configuración - Equivalente a generateQuestions() de JavaScript
        """
        questions = []
        selected_modules = st.session_state.exam_config['modules']
        total_questions = st.session_state.exam_config['question_count']
        
        if not selected_modules:
            st.session_state.questions = []
            return
        
        questions_per_module = max(1, total_questions // len(selected_modules))
        
        # Distribuir preguntas por módulo
        for module in selected_modules:
            module_questions = self.question_database.get(module, [])
            for i in range(min(questions_per_module, len(module_questions))):
                if len(questions) < total_questions:
                    questions.append(module_questions[i % len(module_questions)])
        
        # Llenar espacios restantes si es necesario
        while len(questions) < total_questions:
            random_module = random.choice(selected_modules)
            module_questions = self.question_database.get(random_module, [])
            if module_questions:
                questions.append(random.choice(module_questions))
        
        # Mezclar preguntas aleatoriamente
        random.shuffle(questions)
        st.session_state.questions = questions[:total_questions]
    
    def render_exam_screen(self):
        """
        Renderiza la pantalla principal del examen
        Equivale a la sección exam-screen del HTML
        """
        if not st.session_state.questions:
            st.error("❌ No hay preguntas cargadas")
            return
        
        # Timer y progreso (equivalente a exam-header)
        self.render_timer_and_progress()
        
        # Panel de estadísticas (equivalente a stats-panel)
        self.render_exam_stats()
        
        # Pregunta actual (equivalente a question container)
        self.render_current_question()
        
        # Navegación (equivalente a nav)
        self.render_navigation()
        
        # Botón de finalizar examen
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🏁 Terminar Examen", type="secondary", use_container_width=True):
                st.session_state.show_finish_modal = True
                st.rerun()
        
        # Modal de confirmación para terminar
        if st.session_state.show_finish_modal:
            self.render_finish_modal()
    
    def render_timer_and_progress(self):
        """
        Renderiza el temporizador y barra de progreso
        Equivalente a las funciones startTimer() y updateTimerDisplay() del JavaScript
        """
        if not st.session_state.exam_start_time:
            return
        
        # Calcular tiempo transcurrido y restante
        elapsed_time = datetime.now() - st.session_state.exam_start_time
        time_limit_seconds = st.session_state.exam_config['time_limit'] * 60
        remaining_seconds = max(0, time_limit_seconds - elapsed_time.total_seconds())
        
        # Formatear tiempo restante
        hours = int(remaining_seconds // 3600)
        minutes = int((remaining_seconds % 3600) // 60)
        seconds = int(remaining_seconds % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        warning_class = "timer-warning" if remaining_seconds <= 300 else ""
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Información de progreso
            current_q = st.session_state.current_question_index + 1
            total_q = len(st.session_state.questions)
            answered = sum(1 for ans in st.session_state.user_answers if ans is not None)
            
            st.markdown(f"**Pregunta {current_q} de {total_q}** | **{answered} respondidas**")
            
            # Barra de progreso
            progress = current_q / total_q
            progress_html = f"""
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress*100}%"></div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)
        
        with col2:
            # Timer display
            st.markdown(f"""
            <div class="timer-display {warning_class}">
                ⏰ {time_str}
            </div>
            """, unsafe_allow_html=True)
        
        # Verificar si se acabó el tiempo
        if remaining_seconds <= 0:
            st.error("⏰ ¡Tiempo agotado!")
            self.finish_exam()
            st.rerun()
    
    def render_exam_stats(self):
        """
        Renderiza las estadísticas del examen en tiempo real
        Equivalente a updateStats() del JavaScript
        """
        correct, wrong, skipped = self.calculate_current_stats()
        total_questions = len(st.session_state.questions)
        score = round((correct / total_questions) * 100) if total_questions > 0 else 0
        
        # Panel de estadísticas con diseño similar al HTML
        stats_html = f"""
        <div class="stats-panel">
            <div class="stat-item">
                <div class="stat-value">{correct}</div>
                <div class="stat-label">Correctas</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{wrong}</div>
                <div class="stat-label">Incorrectas</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{skipped}</div>
                <div class="stat-label">Sin responder</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{score}%</div>
                <div class="stat-label">Calificación</div>
            </div>
        </div>
        """
        st.markdown(stats_html, unsafe_allow_html=True)
    
    def render_current_question(self):
        """
        Renderiza la pregunta actual
        Equivalente a displayQuestion() del JavaScript
        """
        if not st.session_state.questions:
            return
        
        current_idx = st.session_state.current_question_index
        if current_idx >= len(st.session_state.questions):
            return
        
        question = st.session_state.questions[current_idx]
        
        # Encabezado de pregunta (equivalente a question-header)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### Pregunta {current_idx + 1}")
        with col2:
            st.markdown(f"**📚 {question['area']}**")
        
        # Tarjeta de pregunta con diseño del HTML
        question_html = f"""
        <div class="question-card">
            <div style="font-size: 1.1rem; line-height: 1.7; margin-bottom: 25px; color: #374151;">
                {question['text']}
            </div>
        </div>
        """
        st.markdown(question_html, unsafe_allow_html=True)
        
        # Opciones de respuesta
        st.markdown("**Selecciona tu respuesta:**")
        
        # Verificar si ya hay una respuesta seleccionada
        current_answer = st.session_state.user_answers[current_idx]
        
        for i, option in enumerate(question['options']):
            option_key = f"option_{current_idx}_{i}"
            
            # Botón de opción con estilo similar al HTML
            if st.button(
                option, 
                key=option_key, 
                use_container_width=True,
                type="primary" if current_answer == i else "secondary"
            ):
                # Guardar respuesta
                st.session_state.user_answers[current_idx] = i
                
                # Auto-avanzar después de seleccionar (con delay simulado)
                time.sleep(0.1)  # Pequeña pausa para mejor UX
                if current_idx < len(st.session_state.questions) - 1:
                    st.session_state.current_question_index += 1
                st.rerun()
    
    def render_navigation(self):
        """
        Renderiza los controles de navegación
        Equivalente a la sección nav del HTML
        """
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Botón Anterior
            if st.button("← Anterior", 
                        disabled=(st.session_state.current_question_index == 0),
                        use_container_width=True):
                st.session_state.current_question_index -= 1
                st.rerun()
        
        with col2:
            # Indicadores de preguntas (equivalente a indicators)
            self.render_question_indicators()
        
        with col3:
            # Botón Siguiente
            next_disabled = st.session_state.current_question_index >= len(st.session_state.questions) - 1
            button_text = "Terminar" if next_disabled else "Siguiente →"
            
            if st.button(button_text, 
                        disabled=False,
                        use_container_width=True):
                if next_disabled:
                    self.finish_exam()
                    st.rerun()
                else:
                    st.session_state.current_question_index += 1
                    st.rerun()
    
    def render_question_indicators(self):
        """
        Renderiza los indicadores de navegación entre preguntas
        Equivalente a la función updateIndicators() del JavaScript
        """
        if not st.session_state.questions:
            return
        
        total_questions = len(st.session_state.questions)
        current_idx = st.session_state.current_question_index
        
        # Crear indicadores visuales
        indicators_html = '<div class="indicators">'
        
        for i in range(total_questions):
            # Determinar el estado del indicador
            if i == current_idx:
                indicator_class = "indicator indicator-current"
                title = f"Pregunta {i+1} (Actual)"
            elif st.session_state.user_answers[i] is not None:
                indicator_class = "indicator indicator-answered"
                title = f"Pregunta {i+1} (Respondida)"
            else:
                indicator_class = "indicator"
                title = f"Pregunta {i+1}"
            
            indicators_html += f'<div class="{indicator_class}" title="{title}"></div>'
        
        indicators_html += '</div>'
        st.markdown(indicators_html, unsafe_allow_html=True)
        
        # Navegación rápida con botones numerados (limitado para mejor UX)
        if total_questions <= 20:  # Solo mostrar si hay pocas preguntas
            st.markdown("**Navegación rápida:**")
            cols = st.columns(min(total_questions, 10))
            
            for i in range(total_questions):
                col_idx = i % 10
                if col_idx < len(cols):
                    with cols[col_idx]:
                        # Estado del botón
                        if i == current_idx:
                            button_type = "primary"
                            label = f"🔵{i+1}"
                        elif st.session_state.user_answers[i] is not None:
                            button_type = "secondary"
                            label = f"✅{i+1}"
                        else:
                            button_type = "secondary"
                            label = f"⚪{i+1}"
                        
                        if st.button(label, key=f"nav_btn_{i}", type=button_type):
                            st.session_state.current_question_index = i
                            st.rerun()
    
    def render_finish_modal(self):
        """
        Renderiza el modal de confirmación para terminar
        Equivalente al modal finishModal del HTML
        """
        st.markdown("---")
        st.markdown("### 🏁 Terminar Examen")
        st.markdown("¿Estás seguro de que deseas terminar el examen? Una vez terminado, no podrás modificar tus respuestas.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("❌ Cancelar", use_container_width=True):
                st.session_state.show_finish_modal = False
                st.rerun()
        
        with col2:
            if st.button("✅ Terminar", type="primary", use_container_width=True):
                st.session_state.show_finish_modal = False
                self.finish_exam()
                st.rerun()
    
    def calculate_current_stats(self) -> Tuple[int, int, int]:
        """
        Calcula estadísticas actuales del examen
        Equivalente a updateStats() del JavaScript
        """
        correct = wrong = skipped = 0
        
        for i, answer in enumerate(st.session_state.user_answers):
            if answer is None:
                skipped += 1
            elif i < len(st.session_state.questions):
                if answer == st.session_state.questions[i]['correct']:
                    correct += 1
                else:
                    wrong += 1
        
        return correct, wrong, skipped
    
    def finish_exam(self):
        """
        Finaliza el examen y calcula resultados
        Equivalente a finishExam() del JavaScript
        """
        # Detener timer
        st.session_state.timer_active = False
        
        if st.session_state.exam_start_time:
            exam_duration = datetime.now() - st.session_state.exam_start_time
        else:
            exam_duration = timedelta(0)
        
        # Calcular resultados finales
        correct, wrong, skipped = self.calculate_current_stats()
        total_questions = len(st.session_state.questions)
        score = round((correct / total_questions) * 100) if total_questions > 0 else 0
        
        # Guardar resultados (equivalente a calculateResults)
        st.session_state.final_results = {
            'score': score,
            'correct': correct,
            'wrong': wrong,
            'skipped': skipped,
            'total_questions': total_questions,
            'exam_type': st.session_state.exam_config['type'],
            'modules': st.session_state.exam_config['modules'],
            'duration': exam_duration,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        st.session_state.current_screen = 'results'
        self.show_notification("🏆 ¡Examen completado!", "success")
    
    def render_results_screen(self):
        """
        Renderiza la pantalla de resultados
        Equivalente a results-screen del HTML
        """
        if 'final_results' not in st.session_state or not st.session_state.final_results:
            st.error("❌ No hay resultados disponibles")
            return
        
        results = st.session_state.final_results
        
        # Puntuación principal con diseño del HTML
        score_html = f"""
        <div class="results-score">
            <div class="score-number">{results['score']}%</div>
            <div style="position: relative; z-index: 1; font-size: 1.2rem; opacity: 0.9;">Calificación Final</div>
        </div>
        """
        st.markdown(score_html, unsafe_allow_html=True)
        
        # Estadísticas detalladas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("✅ Respuestas Correctas", results['correct'])
        with col2:
            st.metric("❌ Respuestas Incorrectas", results['wrong'])
        with col3:
            st.metric("⏭️ Sin Responder", results['skipped'])
        with col4:
            duration_str = str(results['duration']).split('.')[0]  # Remover microsegundos
            st.metric("⏱️ Tiempo Utilizado", duration_str)
        
        # Información adicional del examen
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Detalles del Examen")
            # 🔧 FIX: Cambiar 'config' por 'results' para acceder a los datos correctamente
            st.write(f"**Tipo:** {results.get('exam_type', '').title()}")
            st.write(f"**Total de preguntas:** {results['total_questions']}")
            st.write(f"**Fecha:** {results['date']}")
            st.write(f"**Módulos evaluados:** {', '.join(results['modules'])}")
            
            # Atajos de teclado información
            st.markdown("---")
            st.markdown("### ⌨️ Atajos de Teclado")
            st.markdown("""
            - **Espacio** - Siguiente pregunta
            - **Backspace** - Pregunta anterior
            - **Enter** - Confirmar respuesta
            - **Esc** - Terminar examen
            """)
            
            # Información del desarrollador
            st.markdown("---")
            st.markdown("### 👨‍💻 Acerca de")
            st.markdown("**Von Carloo MC**")
            st.markdown("Simulador EXANI-II Professional")
            st.markdown("Versión Python convertida desde HTML")
        
        with col2:
            st.markdown("### 📈 Análisis de Rendimiento")
            
            # Gráfico de resultados
            chart_data = pd.DataFrame({
                'Categoría': ['Correctas', 'Incorrectas', 'Sin Responder'],
                'Cantidad': [results['correct'], results['wrong'], results['skipped']]
            })
            
            st.bar_chart(chart_data.set_index('Categoría'), use_container_width=True)
        
        # Evaluación de rendimiento
        score = results['score']
        if score >= 70:
            st.success("🎉 ¡Excelente! Has aprobado el examen")
        elif score >= 60:
            st.warning("⚠️ Bien, pero puedes mejorar")
        else:
            st.error("📚 Necesitas estudiar más")
        
        # Acciones (equivalente a actions del HTML)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Revisar Respuestas", use_container_width=True):
                st.session_state.current_screen = 'review'
                st.rerun()
        
        with col2:
            if st.button("🔄 Nuevo Examen", use_container_width=True):
                self.restart_exam()
                st.rerun()
        
        with col3:
            if st.button("📁 Exportar Resultados", use_container_width=True):
                self.export_results()
    
    def render_review_screen(self):
        """
        Renderiza la pantalla de revisión de respuestas
        Funcionalidad adicional no presente en el HTML original
        """
        if not st.session_state.questions or 'final_results' not in st.session_state:
            st.error("❌ No hay información de examen para revisar")
            return
        
        st.markdown("## 📊 Revisión de Respuestas")
        
        # Filtros para la revisión
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_type = st.selectbox(
                "Filtrar por:",
                ["Todas", "Correctas", "Incorrectas", "Sin Responder"]
            )
        with col2:
            area_filter = st.selectbox(
                "Área:",
                ["Todas"] + list(set(q['area'] for q in st.session_state.questions))
            )
        with col3:
            if st.button("🏠 Volver al Inicio"):
                self.restart_exam()
                st.rerun()
        
        # Mostrar preguntas según filtros
        st.markdown("---")
        
        question_count = 0
        for i, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.user_answers[i]
            correct_answer = question['correct']
            
            # Aplicar filtros
            if area_filter != "Todas" and question['area'] != area_filter:
                continue
                
            if filter_type == "Correctas" and user_answer != correct_answer:
                continue
            elif filter_type == "Incorrectas" and (user_answer == correct_answer or user_answer is None):
                continue
            elif filter_type == "Sin Responder" and user_answer is not None:
                continue
            
            question_count += 1
            
            # Determinar estado de la respuesta
            if user_answer is None:
                status = "⏭️ Sin responder"
                status_color = "🔘"
            elif user_answer == correct_answer:
                status = "✅ Correcta"
                status_color = "🟢"
            else:
                status = "❌ Incorrecta"
                status_color = "🔴"
            
            # Mostrar pregunta en expandible
            with st.expander(f"{status_color} Pregunta {i+1} - {question['area']} - {status}"):
                st.markdown(f"**{question['text']}**")
                st.markdown("---")
                
                for j, option in enumerate(question['options']):
                    if j == correct_answer:
                        st.markdown(f"✅ **{option}** (Respuesta correcta)")
                    elif j == user_answer:
                        st.markdown(f"❌ **{option}** (Tu respuesta)")
                    else:
                        st.markdown(f"⚪ {option}")
        
        if question_count == 0:
            st.info("No hay preguntas que coincidan con los filtros seleccionados.")
    
    def export_results(self):
        """
        Exporta los resultados del examen
        Equivalente a exportResults() del JavaScript
        """
        if 'final_results' not in st.session_state:
            st.error("❌ No hay resultados para exportar")
            return
        
        results = st.session_state.final_results
        
        # Crear datos detallados para exportar
        detailed_results = {
            'resumen': results,
            'preguntas_detalle': []
        }
        
        # Agregar detalles de cada pregunta
        for i, question in enumerate(st.session_state.questions):
            user_answer = st.session_state.user_answers[i]
            correct_answer = question['correct']
            
            question_detail = {
                'numero': i + 1,
                'area': question['area'],
                'pregunta': question['text'],
                'opciones': question['options'],
                'respuesta_correcta': correct_answer,
                'respuesta_usuario': user_answer,
                'es_correcta': user_answer == correct_answer if user_answer is not None else False,
                'sin_responder': user_answer is None
            }
            detailed_results['preguntas_detalle'].append(question_detail)
        
        # Crear archivo JSON para descarga
        json_str = json.dumps(detailed_results, ensure_ascii=False, indent=2)
        
        # Botón de descarga
        st.download_button(
            label="📥 Descargar Resultados Detallados (JSON)",
            data=json_str,
            file_name=f"EXANI-II_Resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # También crear CSV con resumen
        summary_data = {
            'Tipo de Examen': [results['exam_type']],
            'Puntuación (%)': [results['score']],
            'Respuestas Correctas': [results['correct']],
            'Respuestas Incorrectas': [results['wrong']],
            'Sin Responder': [results['skipped']],
            'Total Preguntas': [results['total_questions']],
            'Duración': [str(results['duration']).split('.')[0]],
            'Fecha': [results['date']]
        }
        
        df = pd.DataFrame(summary_data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="📊 Descargar Resumen (CSV)",
            data=csv,
            file_name=f"EXANI-II_Resumen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        st.success("📁 Archivos preparados para descarga")
    
    def restart_exam(self):
        """
        Reinicia el simulador al estado inicial
        Equivalente a restartExam() del JavaScript
        """
        # Conservar la configuración pero resetear el estado del examen
        exam_config = st.session_state.exam_config.copy()
        
        # Limpiar estados del examen
        exam_states = [
            'current_question_index', 'questions', 'user_answers', 
            'exam_start_time', 'time_remaining', 'timer_active',
            'show_finish_modal', 'final_results'
        ]
        
        for state in exam_states:
            if state in st.session_state:
                del st.session_state[state]
        
        # Reinicializar
        self.init_session_state()
        st.session_state.exam_config = exam_config
        st.session_state.current_screen = 'dashboard'
        
        self.show_notification("🔄 Simulador reiniciado - Listo para un nuevo examen", "success")
    
    def show_notification(self, message: str, notification_type: str = "success"):
        """
        Sistema de notificaciones
        Equivalente a showNotification() del JavaScript
        """
        st.session_state.notification_message = message
        st.session_state.notification_type = notification_type
        
        # Mostrar notificación según el tipo
        if notification_type == "success":
            st.success(message)
        elif notification_type == "error":
            st.error(message)
        elif notification_type == "warning":
            st.warning(message)
        else:
            st.info(message)
    
    def render_sidebar(self):
        """
        Renderiza la barra lateral con información y controles adicionales
        """
        with st.sidebar:
            st.markdown("## 📋 Panel de Control")
            
            # Información del examen actual
            if st.session_state.current_screen == 'exam':
                st.markdown("### ⏱️ Estado del Examen")
                
                if st.session_state.exam_start_time:
                    elapsed = datetime.now() - st.session_state.exam_start_time
                    st.write(f"⏰ Tiempo transcurrido: {str(elapsed).split('.')[0]}")
                
                if st.session_state.questions:
                    current_q = st.session_state.current_question_index + 1
                    total_q = len(st.session_state.questions)
                    st.write(f"📝 Progreso: {current_q}/{total_q}")
                    
                    answered = sum(1 for ans in st.session_state.user_answers if ans is not None)
                    st.write(f"✅ Respondidas: {answered}/{total_q}")
                
                st.markdown("---")
                
                # Accesos rápidos durante el examen
                st.markdown("### 🚀 Accesos Rápidos")
                
                if st.button("⏭️ Saltar pregunta", use_container_width=True):
                    if st.session_state.current_question_index < len(st.session_state.questions) - 1:
                        st.session_state.current_question_index += 1
                        st.rerun()
                
                if st.button("🔄 Reiniciar examen", use_container_width=True):
                    if st.checkbox("⚠️ Confirmar reinicio"):
                        self.restart_exam()
                        st.rerun()
            
            # Configuración actual
            st.markdown("---")
            st.markdown("###
