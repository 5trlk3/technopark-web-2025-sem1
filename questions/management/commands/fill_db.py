from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from questions.models import User_profile, Question, Answer, Tag, QuestionTag, QuestionLike, AnswerLike
from faker import Faker
import random
from django.db import transaction


class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Multiplication ratio for entities')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        
        self.stdout.write(f'Starting database fill with ratio={ratio}...')
        
        self.stdout.write('Creating users and profiles...')
        profiles = self.create_users(ratio)
        self.stdout.write(self.style.SUCCESS(f'Created {len(profiles)} users and profiles'))
        
        self.stdout.write('Creating tags...')
        tags = self.create_tags(ratio)
        self.stdout.write(self.style.SUCCESS(f'Created {len(tags)} tags'))
        
        self.stdout.write('Creating questions...')
        questions = self.create_questions(ratio * 10, profiles)
        self.stdout.write(self.style.SUCCESS(f'Created {len(questions)} questions'))
        
        self.stdout.write('Linking questions and tags...')
        self.create_question_tags(questions, tags)
        self.stdout.write(self.style.SUCCESS('Linked questions and tags'))
        
        self.stdout.write('Creating answers...')
        answers = self.create_answers(ratio * 100, profiles, questions)
        self.stdout.write(self.style.SUCCESS(f'Created {len(answers)} answers'))
        
        self.stdout.write('Creating likes...')
        self.create_likes(ratio * 200, profiles, questions, answers)
        self.stdout.write(self.style.SUCCESS('Created likes'))
        
        self.stdout.write(self.style.SUCCESS(f'\nDatabase successfully filled!'))
        self.stdout.write(f'Total statistics:')
        self.stdout.write(f'  Users: {ratio}')
        self.stdout.write(f'  Questions: {ratio * 10}')
        self.stdout.write(f'  Answers: {ratio * 100}')
        self.stdout.write(f'  Tags: {ratio}')
        self.stdout.write(f'  Likes: {ratio * 200}')

    def create_users(self, count):
        fake = Faker()
        
        users_to_create = []
        for i in range(count):
            user = User(
                username=f"{fake.user_name()}_{i}",
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            user.set_password('password123')
            users_to_create.append(user)
        
        User.objects.bulk_create(users_to_create)
        
        created_users = list(User.objects.all().order_by('-id')[:count])
        
        profiles_to_create = []
        for user in created_users:
            about = fake.text() if random.random() < 0.5 else ''
            profile = User_profile(
                user_id=user,
                nickname=fake.user_name(),
                image='',
                about=about
            )
            profiles_to_create.append(profile)
        
        User_profile.objects.bulk_create(profiles_to_create)
        
        return list(User_profile.objects.all().order_by('-id')[:count])

    def create_tags(self, count):
        fake = Faker()
        
        tags_to_create = []
        for i in range(count):
            tag_name = f"{fake.word()}_{i}"[:64]
            tag = Tag(name=tag_name)
            tags_to_create.append(tag)
        
        Tag.objects.bulk_create(tags_to_create)
        
        return list(Tag.objects.all().order_by('-id')[:count])

    def create_questions(self, count, profiles):
        fake = Faker()
        
        questions_to_create = []
        for i in range(count):
            title = fake.sentence()[:256]
            text = fake.text(max_nb_chars=1000)
            profile = random.choice(profiles)
            
            question = Question(
                title=title,
                text=text,
                rating=0,
                profile_id=profile
            )
            questions_to_create.append(question)
        
        Question.objects.bulk_create(questions_to_create)
        
        return list(Question.objects.all().order_by('-id')[:count])

    def create_question_tags(self, questions, tags):
        question_tags_to_create = []
        
        for question in questions:
            num_tags = random.randint(1, min(5, len(tags)))
            selected_tags = random.sample(tags, num_tags)
            
            for tag in selected_tags:
                qt = QuestionTag(
                    question_id=question,
                    tag_id=tag
                )
                question_tags_to_create.append(qt)
        
        QuestionTag.objects.bulk_create(question_tags_to_create)

    def create_answers(self, count, profiles, questions):
        fake = Faker()
        
        answers_to_create = []
        for i in range(count):
            text = fake.text(max_nb_chars=500)
            is_correct = random.random() < 0.1
            profile = random.choice(profiles)
            question = random.choice(questions)
            
            answer = Answer(
                text=text,
                is_correct=is_correct,
                rating=0,
                profile_id=profile,
                question_id=question
            )
            answers_to_create.append(answer)
        
        Answer.objects.bulk_create(answers_to_create)
        
        return list(Answer.objects.all().order_by('-id')[:count])

    def create_likes(self, count, profiles, questions, answers):
        question_likes_count = count // 2
        answer_likes_count = count - question_likes_count
        
        question_likes_to_create = []
        used_pairs = set()
        
        attempts = 0
        max_attempts = question_likes_count * 3
        
        while len(question_likes_to_create) < question_likes_count and attempts < max_attempts:
            attempts += 1
            profile = random.choice(profiles)
            question = random.choice(questions)
            pair = (profile.id, question.id)
            
            if pair not in used_pairs:
                used_pairs.add(pair)
                value = 1 if random.random() < 0.7 else -1
                
                ql = QuestionLike(
                    profile_id=profile,
                    question_id=question,
                    value=value
                )
                question_likes_to_create.append(ql)
        
        QuestionLike.objects.bulk_create(question_likes_to_create, ignore_conflicts=True)
        
        answer_likes_to_create = []
        used_pairs = set()
        
        attempts = 0
        max_attempts = answer_likes_count * 3
        
        while len(answer_likes_to_create) < answer_likes_count and attempts < max_attempts:
            attempts += 1
            profile = random.choice(profiles)
            answer = random.choice(answers)
            pair = (profile.id, answer.id)
            
            if pair not in used_pairs:
                used_pairs.add(pair)
                value = 1 if random.random() < 0.7 else -1
                
                al = AnswerLike(
                    profile_id=profile,
                    answer_id=answer,
                    value=value
                )
                answer_likes_to_create.append(al)
        
        AnswerLike.objects.bulk_create(answer_likes_to_create, ignore_conflicts=True)

