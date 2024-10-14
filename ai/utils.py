from openai import OpenAI

from habits.models import Habit, HabitLog, Frequency
from exercises.models import Routine, RoutineExercise, Exercise
from diets.models import Meal, Food, MealFood
from django.core.exceptions import ValidationError
from datetime import date
import os 
from dotenv import load_dotenv
from .models import AI_data
import json 

load_dotenv()


# Mapping for Portuguese to English day names
DAY_MAPPING = {
    "Segunda-feira": "monday",
    "Terça-feira": "tuesday",
    "Quarta-feira": "wednesday",
    "Quinta-feira": "thursday",
    "Sexta-feira": "friday",
    "Sábado": "saturday",
    "Domingo": "sunday"
}

def create_models_data(gpt_data, user):
    # Handle Habits
    habits = gpt_data.get('habits', [])
    for habit_data in habits:
        # Fetch or create frequency objects
        frequencies = Frequency.objects.filter(name__in=[habit_data.get('frequency', 'daily')])

        if not frequencies.exists():
            raise ValidationError(f"Invalid frequency: {habit_data.get('frequency')}")

        # Create habit entry with name and measure in Portuguese
        habit = Habit.objects.create(
            user=user,
            name=habit_data['name'],  # Name in Portuguese
            goal=habit_data['goal'],
            measure=habit_data.get('measure', 'steps')  # Measure in Portuguese
        )
        habit.frequencies.set(frequencies)

        # Optionally create logs for habits if provided
        if 'logs' in habit_data:
            for log in habit_data['logs']:
                HabitLog.objects.create(
                    habit=habit,
                    date=log['date'],
                    amount=log['amount']
                )

    # Handle Exercise Routines
    exercises = gpt_data.get('exercises', [])
    for exercise_data in exercises:
        # Translate Portuguese day to English
        english_day = DAY_MAPPING.get(exercise_data['day'], exercise_data['day'])

        # Create or get the routine
        routine, _ = Routine.objects.get_or_create(
            user=user,
            week_start_date=exercise_data.get('week_start_date', date.today())  # Default to today's date if missing
        )
        
        # Loop through each exercise in the routine
        for routine_data in exercise_data['routine']:
            # Create or get the exercise in Portuguese (but internally stored in English for titles)
            exercise, _ = Exercise.objects.get_or_create(
                name=routine_data['exercise'],  # Name in Portuguese
                exercise_type=routine_data.get('exercise_type', 'gym')  # Default to 'gym' if missing
            )
            
            # Create RoutineExercise entry with the translated day
            RoutineExercise.objects.create(
                routine=routine,
                exercise=exercise,
                day_of_week=english_day,  # Store the English day in the model
                weight_goal=routine_data.get('weight'),
                reps_goal=routine_data.get('reps'),
                duration=routine_data.get('duration'),
                distance=routine_data.get('distance'),
                pace=routine_data.get('pace'),
                average_velocity=routine_data.get('average_velocity')
            )

    # Handle Diet
    diets = gpt_data.get('diet', [])
    for diet_data in diets:
        # Create or get the meal in Portuguese
        meal, _ = Meal.objects.get_or_create(
            user=user,
            name=diet_data['meal'],  # Name of the meal in Portuguese
            date=date.today()  # Assuming you are using today's date
        )
        
        # Add food items to the meal
        for food_item in diet_data.get('foods', []):
            food, _ = Food.objects.get_or_create(
                name=food_item['name'],  # Name of the food in Portuguese
                defaults={
                    'calories': food_item.get('calories', 0),
                    'protein': food_item.get('protein', 0),
                    'carbs': food_item.get('carbs', 0),
                    'fat': food_item.get('fat', 0)
                }
            )
            # Add the food to the meal with servings
            MealFood.objects.create(
                meal=meal,
                food=food,
                servings=food_item.get('servings', 1)  # Default servings to 1 if not provided
            )

def generate_data_with_gpt(data):
    try:    
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                "role": "system",
                "content": """
                Você é um assistente de IA que gera hábitos saudáveis personalizados, rotinas de exercícios e planos alimentares com base nos dados do usuário. 
                Responda **APENAS** com a estrutura JSON, sem explicações ou texto adicional, e forneça os nomes, títulos e descrições em português, como descrito a seguir:

                - Para os **hábitos**: O nome do hábito e a unidade de medida devem estar em português. **Certifique-se de gerar pelo menos três hábitos: um relacionado ao sono, um à alimentação e outro à prática de exercícios.**
                - Para os **exercícios**: O nome do exercício e o título devem estar em português. **Certifique-se de gerar pelo menos três exercícios para cada dia disponível (it will come in available days key in the json that i will send).**
                - Para a **dieta**: Liste cada refeição em português com os alimentos incluídos, suas quantidades, calorias, proteínas, carboidratos e gorduras. **Certifique-se de incluir pelo menos três refeições para o dia.**
                - Para os **dias da semana**: Use os dias em português (segunda-feira, terça-feira, etc.).

                A estrutura de resposta deve ser assim:
                {
                    "habits": [
                        {
                            "name": "Dormir bem",  # Nome do hábito em português
                            "goal": 8,
                            "measure": "horas"  # Unidade de medida em português
                        },
                        {
                            "name": "Comer frutas diariamente",  # Nome relacionado à alimentação
                            "goal": 3,
                            "measure": "porções"  # Unidade de medida em português
                        },
                        {
                            "name": "Exercitar-se regularmente",  # Nome relacionado a exercícios
                            "goal": 5,
                            "measure": "dias por semana"  # Unidade de medida em português
                        },
                        ...
                    ],
                    "exercises": [
                        {
                            "day": "Segunda-feira",  # O dia da semana em português
                            "routine": [
                                {
                                    "exercise": "Agachamento com barra",  # Nome do exercício em português
                                    "sets": 3,
                                    "weight": 20
                                    "reps": 15,
                                    "title": "Agachamento"  # Título em português
                                },
                                {
                                    "exercise": "Supino reto",  # Segundo exercício
                                    "sets": 3,
                                    "weight": 30
                                    "reps": 12,
                                    "title": "Supino"
                                },
                                {
                                    "exercise": "Levantamento terra",  # Terceiro exercício
                                    "sets": 3,
                                    "weight": 40
                                    "reps": 10,
                                    "title": "Levantamento"
                                }
                            ]
                        },
                        ...
                    ],
                    "diet": [
                        {
                            "meal": "Café da manhã",  # Nome da refeição em português
                            "foods": [  # Lista de alimentos com detalhes
                                {
                                    "name": "Claras de ovos",  # Nome do alimento
                                    "servings": 2,  # Quantidade de porções
                                    "calories": 34,  # Calorias por porção
                                    "protein": 7.2,  # Proteína em gramas por porção
                                    "carbs": 0.2,  # Carboidratos em gramas por porção
                                    "fat": 0.1  # Gordura em gramas por porção
                                },
                                {
                                    "name": "Aveia",
                                    "servings": 1,
                                    "calories": 150,
                                    "protein": 5,
                                    "carbs": 27,
                                    "fat": 3
                                },
                                {
                                    "name": "Banana",
                                    "servings": 1,
                                    "calories": 89,
                                    "protein": 1.1,
                                    "carbs": 23,
                                    "fat": 0.3
                                }
                            ]
                        },
                        {
                            "meal": "Almoço",  # Segunda refeição
                            "foods": [ ... ]
                        },
                        {
                            "meal": "Jantar",  # Terceira refeição
                            "foods": [ ... ]
                        },
                        ...
                    ]
                }
                Lembre-se de fornecer apenas a estrutura JSON válida, sem texto adicional. Todas as informações solicitadas devem estar em português.
                """
                }, {"role": "user", "content": f"User Data: {data}"}
            ]
        )
        
        response_content = completion.choices[0].message.content
        
        # Parse the response content as JSON
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            raise ValueError("GPT returned a response that is not valid JSON")

    except Exception as e:
        print(f"An error occurred while generating data with GPT: {e}")
        return None

def get_data(data):
    """
    Description: if there is data for the goal, return it. Otherwise, request AI, save in DB and return it.
    """

    goal = data.get('goal', '')

    if not goal:
        return None 
    
    data_for_goal_exists = AI_data.objects.filter(goal=goal).exists()

    print("data_for_goal_exists", data_for_goal_exists)

    if data_for_goal_exists:
        print("returning existing data")
        return AI_data.objects.get(goal=goal).json_data
    else:
        print("fetching data")
        gpt_data = generate_data_with_gpt(data)

        print(gpt_data)
        
        dict_data = {
            'goal': goal,
            'json_data': gpt_data
        }
        print("registering response")
        AI_data.objects.create(**dict_data)
        return gpt_data
    



