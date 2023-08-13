from flask_restful import Resource, reqparse
from models import db, Tutor, Pet, TutorSchema, PetSchema
from flask import request

tutor_schema = TutorSchema()
tutors_schema = TutorSchema(many=True)

pet_schema = PetSchema()
pets_schema = PetSchema(many=True)

class TutorResource(Resource):
    def get(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if tutor:
            return tutor_schema.dump(tutor)
        return {'messagem': 'Tutor não encontrado'}, 404
    
    def put(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return {'mensagem': 'Tutor não encontrado'}, 404
        
        data = request.get_json()
        if 'nome' in data:
            tutor.nome = data['nome']
        
        db.session.commit()
        return tutor_schema.dump(tutor)
    
    def delete(self, tutor_id):
        tutor = Tutor.query.get(tutor_id)
        if not tutor:
            return {'mensagem': 'Tutor não encontrado'}, 404
        
        db.session.delete(tutor)
        db.session.commit()
        return {'mensagem': 'Tutor excluído'}

class PetResource(Resource):
    def get(self, pet_id):
        pet = Pet.query.get(pet_id)
        if pet:
            return pet_schema.dump(pet)
        return {'mensagem': 'Pet não encontrado'}, 404
    
    def put(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return {'mensagem': 'Pet não encontrado'}, 404
        
        data = request.get_json()
        if 'nome' in data:
            pet.nome = data['nome']
        if 'tutor_id' in data:
            pet.tutor_id = data['tutor_id']
        
        db.session.commit()
        return pet_schema.dump(pet)
    
    def delete(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return {'mensagem': 'Pet não encontrado'}, 404
        
        db.session.delete(pet)
        db.session.commit()
        return {'mensagem': 'Pet excluído'}
    
    def post(self):
        data = request.get_json()
        nome = data.get('nome')
        tutor_id = data.get('tutor_id')
        
        if not nome or not tutor_id:
            return {'mensagem': 'Dados obrigatórios faltando'}, 400
        
        new_pet = Pet(nome=nome, tutor_id=tutor_id)
        db.session.add(new_pet)
        db.session.commit()
        
        return pet_schema.dump(new_pet), 201
