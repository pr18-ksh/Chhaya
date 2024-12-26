from datetime import datetime
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.db.models import Q
from .pagination import paginate
from .serializers import CaseReportSerializer, ChowkiSerializer, DivisionNestedSerializer, HospitalDivisionSerializer, HospitalSerializer, HospitalZoneSerializer, MissingPersonSerializer, PoliceStationNestedSerializer, UndefinedMissingpersonSerializer, UnidentifiedBodySerializer, VolunteerSerializer, ZoneSerializer
from rest_framework import status
from .models import CaseReport, Chowki, Division, Hospital, HospitalDivision, HospitalZone, MatchedRecord, MissingPerson, PoliceStation, ResolvedCase, UnidentifiedBody, UnidentifiedMissingPerson, Volunteer,Match, Zone
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator

# api for the all persons 
class MissingPersonAPIView(APIView):

    def get(self, request, missing_person_id=None):
        try:
            if missing_person_id is not None:
                try:
                    missing_person = MissingPerson.objects.get(pk=missing_person_id, is_deleted=False)
                    serializer = MissingPersonSerializer(missing_person)
                    return Response(serializer.data)
                except MissingPerson.DoesNotExist:
                    return Response({"error": "Missing person not found"}, status=status.HTTP_404_NOT_FOUND)

            search_query = request.GET.get('search', '')
            if search_query:
                missing_persons = MissingPerson.objects.filter(is_deleted=False).filter(
                Q(full_name__icontains=search_query) | 
                Q(description__icontains=search_query)  
                ).order_by('-id')
            else:
                missing_persons = MissingPerson.objects.filter(is_deleted=False).order_by('-id')

            page_size = int(request.GET.get('page_size', 5))  
            paginator = Paginator(missing_persons, page_size)
            page_number = request.GET.get('page', 1)  
            page_obj = paginator.get_page(page_number)

            serializer = MissingPersonSerializer(page_obj, many=True)

            return Response({
                'data': serializer.data,
                'pagination': {
                    'total_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'total_entries': paginator.count,
                    'page_size': page_size
                }
            })

        except Exception as e:
            return Response({'msg': 'Something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            serializer = MissingPersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, missing_person_id):
        try:
            missing_person = MissingPerson.objects.get(pk=missing_person_id, is_deleted=False)
            serializer = MissingPersonSerializer(missing_person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MissingPerson.DoesNotExist:
            return Response({"error": "Missing person not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, missing_person_id):
        try:
            missing_person = MissingPerson.objects.get(pk=missing_person_id, is_deleted=False)
            missing_person.is_deleted = True
            missing_person.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MissingPerson.DoesNotExist:
            return Response({"error": "Missing person not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnidentifiedMissingperson(APIView):

    def get(self, request, undefined_missing_person_id=None):
        if undefined_missing_person_id is not None:
            try:
                # Fetch a single missing person based on the ID
                undefined_missing_person = UnidentifiedMissingPerson.objects.get(pk=undefined_missing_person_id, is_deleted=False)
                serializer = UndefinedMissingpersonSerializer(undefined_missing_person)
                return Response(serializer.data)
            except UnidentifiedMissingPerson.DoesNotExist:
                return Response({"error": "Undefined missing person not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            undefined_missing_persons = UnidentifiedMissingPerson.objects.filter(is_deleted=False).order_by('-id')
            page_size = int(request.GET.get('page_size', 5))  
            page_number = request.GET.get('page', 1)  
            paginator = Paginator(undefined_missing_persons, page_size)
            page_obj = paginator.get_page(page_number)

            serializer = UndefinedMissingpersonSerializer(page_obj, many=True)

            return Response({
                'data': serializer.data,
                'pagination': {
                    'total_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'total_entries': paginator.count,
                    'page_size': page_size
                }
            })

        except Exception as e:
            return Response({'msg': 'Something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = UndefinedMissingpersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, undefined_missing_person_id):
        try:
            undefined_missing_person = UnidentifiedMissingPerson.objects.get(pk=undefined_missing_person_id, is_deleted=False)
            serializer = UndefinedMissingpersonSerializer(undefined_missing_person, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UnidentifiedMissingPerson.DoesNotExist:
            return Response({"error": "Undefined missing person not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, undefined_missing_person_id):
        try:
            undefined_missing_person = UnidentifiedMissingPerson.objects.get(pk=undefined_missing_person_id, is_deleted=False)
            undefined_missing_person.is_deleted = True
            undefined_missing_person.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UnidentifiedMissingPerson.DoesNotExist:
            return Response({"error": "Undefined missing person not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnidentifiedBodyAPIView(APIView):

    def get(self, request, unidentified_body_id=None):
        if unidentified_body_id is not None:
            try:
                unidentified_body = UnidentifiedBody.objects.get(pk=unidentified_body_id, is_deleted=False)
                serializer = UnidentifiedBodySerializer(unidentified_body)
                return Response(serializer.data)
            except UnidentifiedBody.DoesNotExist:
                return Response({"error": "Unidentified body not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            unidentified_bodies = UnidentifiedBody.objects.filter(is_deleted=False).order_by('-id')
            page_size = int(request.GET.get('page_size', 5))  
            page_number = request.GET.get('page', 1) 
            paginator = Paginator(unidentified_bodies, page_size)
            page_obj = paginator.get_page(page_number)

            serializer = UnidentifiedBodySerializer(page_obj, many=True)

            return Response({
                'data': serializer.data,
                'pagination': {
                    'total_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'total_entries': paginator.count,
                    'page_size': page_size
                }
            })

        except Exception as e:
            return Response({'msg': 'Something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = UnidentifiedBodySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, unidentified_body_id):
        try:
            unidentified_body = UnidentifiedBody.objects.get(pk=unidentified_body_id, is_deleted=False)
            serializer = UnidentifiedBodySerializer(unidentified_body, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Unidentified body not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, unidentified_body_id):
        try:
            unidentified_body = UnidentifiedBody.objects.get(pk=unidentified_body_id, is_deleted=False)
            unidentified_body.is_deleted = True
            unidentified_body.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": "Unidentified body not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VolunteerAPIView(APIView):

    def get(self, request, volunteer_id=None):
        if volunteer_id is not None:
            try:
                volunteer = Volunteer.objects.get(pk=volunteer_id, is_deleted=False)
                serializer = VolunteerSerializer(volunteer)
                return Response(serializer.data)
            except Volunteer.DoesNotExist:
                return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            volunteers = Volunteer.objects.filter(is_deleted=False).order_by('-id')
            page_size = int(request.GET.get('page_size', 5))
            page_number = request.GET.get('page', 1)
            paginator = Paginator(volunteers, page_size)
            page_obj = paginator.get_page(page_number)
            serializer = VolunteerSerializer(page_obj, many=True)

            return Response({
                'data': serializer.data,
                'pagination': {
                    'total_pages': paginator.num_pages,
                    'current_page': page_obj.number,
                    'has_next': page_obj.has_next(),
                    'has_previous': page_obj.has_previous(),
                    'total_entries': paginator.count,
                    'page_size': page_size
                }
            })

        except Exception as e:
            return Response({'msg': 'Something went wrong', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = VolunteerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, volunteer_id):
        try:
            volunteer = Volunteer.objects.get(pk=volunteer_id, is_deleted=False)
            serializer = VolunteerSerializer(volunteer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, volunteer_id):
        try:
            volunteer = Volunteer.objects.get(pk=volunteer_id, is_deleted=False)
            volunteer.is_deleted = True
            volunteer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"error": "Volunteer not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchIndividualMatches(APIView):
    def get(self, request):
        # Get the missing person's name or ID from query parameters
        missing_person_name = request.query_params.get('name', '').strip()
        if not missing_person_name:
            return Response({"error": "Missing person name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the specific missing person by name (or implement additional logic for ID if needed)
        try:
            missing_person = MissingPerson.objects.get(full_name__icontains=missing_person_name, is_deleted=False)
        except MissingPerson.DoesNotExist:
            return Response({"error": "No missing person found with the provided name"}, status=status.HTTP_404_NOT_FOUND)

        # Fetch manually rejected matches for this missing person
        rejected_matches = Match.objects.filter(missing_person=missing_person,rejected=True)

        # Exclude rejected matches from unidentified missing persons and bodies
        rejected_missing_person_ids = rejected_matches.values_list('undefined_missing_person_id',flat=True)
        rejected_body_ids = rejected_matches.values_list('unidentified_body_id',flat=True)

        unidentified_missing_people = UnidentifiedMissingPerson.objects.filter(is_deleted=False).exclude(id__in=rejected_missing_person_ids)
        unidentified_bodies = UnidentifiedBody.objects.filter(is_deleted=False).exclude(id__in=rejected_body_ids)

        # Results list to store match information
        results = []

        # Match with unidentified missing persons
        for undefined_missing_person in unidentified_missing_people:
            is_match, match_percentage = self.is_match_with_undefined_missing_person(missing_person, undefined_missing_person)
            if is_match:
                results.append({
                    'missing_person': MissingPersonSerializer(missing_person).data,
                    'undefined_missing_person': UndefinedMissingpersonSerializer(undefined_missing_person).data,
                    'match_type': 'Missing Person vs Undefined Missing Person',
                    'match_percentage': round(match_percentage, 2),
                })

        # Match with unidentified bodies
        for unidentified_body in unidentified_bodies:
            is_match, match_percentage = self.is_match_with_unidentified_body(missing_person, unidentified_body)
            if is_match:
                results.append({
                    'missing_person': MissingPersonSerializer(missing_person).data,
                    'unidentified_body': UnidentifiedBodySerializer(unidentified_body).data,
                    'match_type': 'Missing Person vs Unidentified Dead Body',
                    'match_percentage': round(match_percentage, 2),
                })

        response_data = {
            'message': 'Matches found' if results else 'No matches found',
            'results': results
        }
        return Response(response_data, status=status.HTTP_200_OK if results else status.HTTP_404_NOT_FOUND)
    
    def is_match_with_undefined_missing_person(self, missing_person, undefined_missing_person):
        match_score = 0
        total_checks = 0

        if missing_person.full_name and undefined_missing_person.full_name:
            total_checks += 1
            if missing_person.full_name.lower() == undefined_missing_person.full_name.lower():
                match_score += 1

        if missing_person.age and undefined_missing_person.estimated_age:
            total_checks += 1
            if abs(missing_person.age - undefined_missing_person.estimated_age) <= 5:
                match_score += 1

                # 3. Gender - Exact Match
        if missing_person.gender and undefined_missing_person.gender:
            total_checks += 1
            if missing_person.gender == undefined_missing_person.gender:
                match_score += 1

        # 4. Height - Approximate Match
        if missing_person.height and undefined_missing_person.height:
            total_checks += 1
            if abs(missing_person.height - undefined_missing_person.height) <= 5:  # Allow height range ±5 cm
                match_score += 1

        # 5. Weight - Approximate Match
        if missing_person.weight and undefined_missing_person.weight:
            total_checks += 1
            if abs(missing_person.weight - undefined_missing_person.weight) <= 5:  # Allow weight range ±5 kg
                match_score += 1

        # 6. Complexion - Exact Match
        if missing_person.complexion and undefined_missing_person.complexion:
            total_checks += 1
            if missing_person.complexion.lower() == undefined_missing_person.complexion.lower():
                match_score += 1

        # 7. Hair Color - Exact Match
        if missing_person.hair_color and undefined_missing_person.hair_color:
            total_checks += 1
            if missing_person.hair_color.lower() == undefined_missing_person.hair_color.lower():
                match_score += 1

        # 8. Hair Type - Exact Match
        if missing_person.hair_type and undefined_missing_person.hair_type:
            total_checks += 1
            if missing_person.hair_type.lower() == undefined_missing_person.hair_type.lower():
                match_score += 1

        # 9. Eye Color - Exact Match
        if missing_person.eye_color and undefined_missing_person.eye_color:
            total_checks += 1
            if missing_person.eye_color.lower() == undefined_missing_person.eye_color.lower():
                match_score += 1

        # 10. Birth Mark - Exact Match
        if missing_person.birth_mark and undefined_missing_person.birth_mark:
            total_checks += 1
            if missing_person.birth_mark.lower() == undefined_missing_person.birth_mark.lower():
                match_score += 1

        # 11. Other Distinctive Marks - Exact Match
        if missing_person.distinctive_mark and undefined_missing_person.other_distinctive_mark:
            total_checks += 1
            if missing_person.distinctive_mark.lower() == undefined_missing_person.other_distinctive_mark.lower():
                match_score += 1

        # 12. Last Location of Missing Person vs Location Found - Geographic Proximity
        if missing_person.last_seen_location and undefined_missing_person.last_seen_details:
            total_checks += 1
            if missing_person.last_seen_location.lower() == undefined_missing_person.last_seen_details.lower():
                match_score += 1

        # 13. Caste - Exact Match
        if missing_person.caste and undefined_missing_person.caste:
            total_checks += 1
            if missing_person.caste.lower() == undefined_missing_person.caste.lower():
                match_score += 1

        # 14. photo - Exact Match
        # if missing_person.photo_upload and UndefinedMissingPerson.photo_upload:
        #     total_checks += 1
        #     image1_path = str(missing_person.photo_upload.path)
        #     image2_path = str(UndefinedMissingPerson.photo_upload.path)

        #     if os.path.exists(image1_path) and os.path.exists(image2_path):
        #         if is_face_match(image1_path, image2_path):
        #             match_score += 1

        # 15. Identification Details - Direct Verification (e.g., Aadhar, PAN)
        if missing_person.identification_card_no and undefined_missing_person.identification_details:
            total_checks += 1
            if missing_person.identification_card_no == undefined_missing_person.identification_details:
                match_score += 1
        
        # if missing_person.Condition and UndefinedMissingPerson.condition_at_discovery:
        #     total_checks += 1
        #     if missing_person.Condition == UndefinedMissingPerson.condition_at_discovery:
        #         match_score += 1

        # Match percentage 
        match_percentage = (match_score / total_checks) * 100 if total_checks > 0 else 0
        return match_percentage >= 60, match_percentage

    def is_match_with_unidentified_body(self, missing_person, unidentified_body):
        match_score = 0
        total_checks = 0

        if missing_person.full_name and unidentified_body.full_name:
            total_checks += 1
            if missing_person.full_name.lower() == unidentified_body.full_name.lower():
                match_score += 1

        if missing_person.age and unidentified_body.estimated_age:
            total_checks += 1
            if abs(missing_person.age - unidentified_body.estimated_age) <= 5:
                match_score += 1
        
                if missing_person.gender and unidentified_body.gender:
                   total_checks += 1
                if missing_person.gender == unidentified_body.gender:
                   match_score += 1

        # 4. Height - Approximate Match
        if missing_person.height and unidentified_body.height:
            total_checks += 1
            if abs(missing_person.height - unidentified_body.height) <= 5:  # Allow height range ±5 cm
                match_score += 1

        # 5. Weight - Approximate Match
        if missing_person.weight and unidentified_body.weight:
            total_checks += 1
            if abs(missing_person.weight - unidentified_body.weight) <= 5:  # Allow weight range ±5 kg
                match_score += 1

        # 6. Complexion - Exact Match
        if missing_person.complexion and unidentified_body.complexion:
            total_checks += 1
            if missing_person.complexion.lower() == unidentified_body.complexion.lower():
                match_score += 1

        # 7. Hair Color - Exact Match
        if missing_person.hair_color and unidentified_body.hair_color:
            total_checks += 1
            if missing_person.hair_color.lower() == unidentified_body.hair_color.lower():
                match_score += 1

        # 8. Hair Type - Exact Match
        if missing_person.hair_type and unidentified_body.hair_type:
            total_checks += 1
            if missing_person.hair_type.lower() == unidentified_body.hair_type.lower():
                match_score += 1

        # 9. Eye Color - Exact Match
        if missing_person.eye_color and unidentified_body.eye_color:
            total_checks += 1
            if missing_person.eye_color.lower() == unidentified_body.eye_color.lower():
                match_score += 1

        # 10. Birth Mark - Exact Match
        if missing_person.birth_mark and unidentified_body.birth_mark:
            total_checks += 1
            if missing_person.birth_mark.lower() == unidentified_body.birth_mark.lower():
                match_score += 1

        # 11. Other Distinctive Marks - Exact Match
        if missing_person.distinctive_mark and unidentified_body.other_distinctive_mark:
            total_checks += 1
            if missing_person.distinctive_mark.lower() == unidentified_body.other_distinctive_mark.lower():
                match_score += 1

        # 12. Last Location of Missing Person vs Location Found - Geographic Proximity
        if missing_person.last_seen_location and unidentified_body.last_seen_details:
            total_checks += 1
            if missing_person.last_seen_location.lower() == unidentified_body.last_seen_details.lower():
                match_score += 1


        # 14. Photo Upload - Visual Match (optional, requires external visual comparison)
        if missing_person.photo_upload and unidentified_body.body_photo_upload:
            total_checks += 1
            if missing_person.photo_upload == unidentified_body.body_photo_upload:
                match_score += 1    

        match_percentage = (match_score / total_checks) * 100 if total_checks > 0 else 0
        return match_percentage >= 60, match_percentage

class RejectMatchAPIView(APIView):
    def post(self, request):
        # Extract parameters
        missing_person_id = request.data.get('missing_person_id')
        unidentified_missing_person_id = request.data.get('unidentified_missing_person_id')
        unidentified_body_id = request.data.get('unidentified_body_id')
        rejection_reason = request.data.get("rejection_reason", "Manual Rejection")
        match_percentage = request.data.get("match_percentage", 0)
        
        if not missing_person_id:
            return Response({"error": "Missing person ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            missing_person = MissingPerson.objects.get(id=missing_person_id, is_deleted=False)
        except MissingPerson.DoesNotExist:
            return Response({"error": "Missing person not found"}, status=status.HTTP_404_NOT_FOUND)

        if not unidentified_missing_person_id and not unidentified_body_id:
            return Response({"error": "Either unidentified missing person ID or unidentified body ID is required"},
                            status=status.HTTP_400_BAD_REQUEST)

       
        # Handle rejection for unidentified missing persons
        if unidentified_missing_person_id:
            try:
                unidentified_person = UnidentifiedMissingPerson.objects.get(id=unidentified_missing_person_id, is_deleted=False)
            except UnidentifiedMissingPerson.DoesNotExist:
                return Response({"error": "Unidentified missing person not found"}, status=status.HTTP_404_NOT_FOUND)

            match, created = Match.objects.get_or_create(
                missing_person=missing_person,
                undefined_missing_person=unidentified_person,
                defaults={
                    "rejection_reason": rejection_reason,
                    "match_percentage": match_percentage,
                    "rejected": True,
                    "match_status": "Rejected",
                },
            )
            if not created:
                match.rejected = True
                match.rejection_reason = rejection_reason
                match.match_status = "Rejected"
                match.save()

        
        # Handle rejection for unidentified bodies
        if unidentified_body_id:
            try:
                unidentified_body = UnidentifiedBody.objects.get(id=unidentified_body_id, is_deleted=False)
            except UnidentifiedBody.DoesNotExist:
                return Response({"error": "Unidentified body not found"}, status=status.HTTP_404_NOT_FOUND)

            match, created = Match.objects.get_or_create(
                missing_person=missing_person,
                unidentified_body=unidentified_body,
                defaults={
                    "rejection_reason": rejection_reason,
                    "match_percentage": match_percentage,
                    "rejected": True,
                    "match_status": "Rejected",
                },
            )
            if not created:
                match.rejected = True
                match.rejection_reason = rejection_reason
                match.match_status = "Rejected"
                match.save()

        return Response({"message": "Match rejected successfully"}, status=status.HTTP_200_OK)
    
# api to search the matching
# class SearchAllMatches(APIView):
#     def get(self, request):
#         results = []
#         matches_to_create = []

#         missing_people = MissingPerson.objects.filter(is_deleted=False)
#         undefined_missing_people = UnidentifiedMissingPerson.objects.filter(is_deleted=False)
#         unidentified_bodies = UnidentifiedBody.objects.filter(is_deleted=False)


#         existing_matches = Match.objects.filter(
#             missing_person__in=missing_people,
#             rejected=False 
#         )

#         for match in existing_matches:
#             match_details = {
#                 'missing_person': MissingPersonSerializer(match.missing_person).data,
#                 'match_percentage': match.match_percentage,
#                 'match_type': 'Existing' if match.undefined_missing_person else 'Existing with Unidentified Dead Body'
#             }
#             if match.undefined_missing_person:
#                 match_details['undefined_missing_person'] = UndefinedMissingpersonSerializer(match.undefined_missing_person).data
#             elif match.unidentified_body:
#                 match_details['unidentified_body'] = UnidentifiedBodySerializer(match.unidentified_body).data

#             results.append(match_details)

#         for missing_person in missing_people:
#             for undefined_missing_person in undefined_missing_people:
#                 is_match,match_percentage=self.is_match_with_undefined_missing_person(missing_person, undefined_missing_person)

#                 if is_match:
#                     if not existing_matches.filter(
#                         missing_person=missing_person,
#                         undefined_missing_person=undefined_missing_person,
#                         # rejected=False 
#                     ).exists():
#                         match_details = {
#                             'missing_person': MissingPersonSerializer(missing_person).data,
#                             'undefined_missing_person': UndefinedMissingpersonSerializer(undefined_missing_person).data,
#                             'match_type': 'Missing Person vs Undefined Missing Person',
#                             'match_percentage': round(match_percentage, 2),
#                         }
#                         results.append(match_details)
#                         matches_to_create.append(Match(
#                             missing_person=missing_person,
#                             undefined_missing_person=undefined_missing_person,
#                             match_percentage=round(match_percentage, 2)
#                         ))

#             for unidentified_body in unidentified_bodies:
#                 is_match, match_percentage = self.is_match_with_unidentified_body(missing_person, unidentified_body)

#                 if is_match:
#                     if not existing_matches.filter(
#                         missing_person=missing_person,
#                         unidentified_body=unidentified_body
#                     ).exists():
#                         match_details = {
#                             'missing_person': MissingPersonSerializer(missing_person).data,
#                             'unidentified_body': UnidentifiedBodySerializer(unidentified_body).data,
#                             'match_type': 'Missing Person vs Unidentified Dead Body',
#                             'match_percentage': round(match_percentage, 2),
#                             # 'rejected': match.rejected 
#                         }
#                         results.append(match_details)
#                         matches_to_create.append(Match(
#                             missing_person=missing_person,
#                             unidentified_body=unidentified_body,
#                             match_percentage=round(match_percentage, 2)
#                         ))

#         if matches_to_create:
#             Match.objects.bulk_create(matches_to_create)

#         match_count = len(results)
#         response_data = {
#             'message': 'Matches found' if results else 'No matches found',
#             'match_count': match_count,
#             'results': results
#         }

#         return Response(response_data, status=status.HTTP_200_OK if results else status.HTTP_404_NOT_FOUND)

#     def is_match_with_undefined_missing_person(self, missing_person, UndefinedMissingPerson):
#         match_score = 0
#         total_checks = 0

#         # 1. Full Name - Exact/Partial Match
#         if missing_person.full_name and UndefinedMissingPerson.full_name:
#             total_checks += 1
#             if missing_person.full_name.lower() == UndefinedMissingPerson.full_name.lower():
#                 match_score += 1  # Exact match
#             elif missing_person.full_name.lower() in UndefinedMissingPerson.full_name.lower() or UndefinedMissingPerson.full_name.lower() in missing_person.full_name.lower():
#                 match_score += 0.5  # Partial match

#         # 2. Age - Approximate Match
#         if missing_person.age is not None and UndefinedMissingPerson.estimated_age is not None:
#             total_checks += 1
#             if abs(missing_person.age - UndefinedMissingPerson.estimated_age) <= 5:  # Allow age range ±5
#                 match_score += 1

        # 3. Gender - Exact Match
        # if missing_person.gender and UndefinedMissingPerson.gender:
        #     total_checks += 1
        #     if missing_person.gender == UndefinedMissingPerson.gender:
        #         match_score += 1

        # # 4. Height - Approximate Match
        # if missing_person.height and UndefinedMissingPerson.height:
        #     total_checks += 1
        #     if abs(missing_person.height - UndefinedMissingPerson.height) <= 5:  # Allow height range ±5 cm
        #         match_score += 1

        # # 5. Weight - Approximate Match
        # if missing_person.weight and UndefinedMissingPerson.weight:
        #     total_checks += 1
        #     if abs(missing_person.weight - UndefinedMissingPerson.weight) <= 5:  # Allow weight range ±5 kg
        #         match_score += 1

        # # 6. Complexion - Exact Match
        # if missing_person.complexion and UndefinedMissingPerson.complexion:
        #     total_checks += 1
        #     if missing_person.complexion.lower() == UndefinedMissingPerson.complexion.lower():
        #         match_score += 1

        # # 7. Hair Color - Exact Match
        # if missing_person.hair_color and UndefinedMissingPerson.hair_color:
        #     total_checks += 1
        #     if missing_person.hair_color.lower() == UndefinedMissingPerson.hair_color.lower():
        #         match_score += 1

        # # 8. Hair Type - Exact Match
        # if missing_person.hair_type and UndefinedMissingPerson.hair_type:
        #     total_checks += 1
        #     if missing_person.hair_type.lower() == UndefinedMissingPerson.hair_type.lower():
        #         match_score += 1

        # # 9. Eye Color - Exact Match
        # if missing_person.eye_color and UndefinedMissingPerson.eye_color:
        #     total_checks += 1
        #     if missing_person.eye_color.lower() == UndefinedMissingPerson.eye_color.lower():
        #         match_score += 1

        # # 10. Birth Mark - Exact Match
        # if missing_person.birth_mark and UndefinedMissingPerson.birth_mark:
        #     total_checks += 1
        #     if missing_person.birth_mark.lower() == UndefinedMissingPerson.birth_mark.lower():
        #         match_score += 1

        # # 11. Other Distinctive Marks - Exact Match
        # if missing_person.distinctive_mark and UndefinedMissingPerson.other_distinctive_mark:
        #     total_checks += 1
        #     if missing_person.distinctive_mark.lower() == UndefinedMissingPerson.other_distinctive_mark.lower():
        #         match_score += 1

        # # 12. Last Location of Missing Person vs Location Found - Geographic Proximity
        # if missing_person.last_seen_location and UndefinedMissingPerson.last_seen_details:
        #     total_checks += 1
        #     if missing_person.last_seen_location.lower() == UndefinedMissingPerson.last_seen_details.lower():
        #         match_score += 1

        # # 13. Caste - Exact Match
        # if missing_person.caste and UndefinedMissingPerson.caste:
        #     total_checks += 1
        #     if missing_person.caste.lower() == UndefinedMissingPerson.caste.lower():
        #         match_score += 1

        # # 14. photo - Exact Match
        # # if missing_person.photo_upload and UndefinedMissingPerson.photo_upload:
        # #     total_checks += 1
        # #     image1_path = str(missing_person.photo_upload.path)
        # #     image2_path = str(UndefinedMissingPerson.photo_upload.path)

        # #     if os.path.exists(image1_path) and os.path.exists(image2_path):
        # #         if is_face_match(image1_path, image2_path):
        # #             match_score += 1

        # # 15. Identification Details - Direct Verification (e.g., Aadhar, PAN)
        # if missing_person.identification_card_no and UndefinedMissingPerson.identification_details:
        #     total_checks += 1
        #     if missing_person.identification_card_no == UndefinedMissingPerson.identification_details:
        #         match_score += 1
        
        # # if missing_person.Condition and UndefinedMissingPerson.condition_at_discovery:
        # #     total_checks += 1
        # #     if missing_person.Condition == UndefinedMissingPerson.condition_at_discovery:
        # #         match_score += 1

        # # Match percentage
        # match_percentage = (match_score / total_checks) * 100 if total_checks > 0 else 0
        # return match_percentage >= 60, match_percentage

#     def is_match_with_unidentified_body(self, missing_person, UnidentifiedBody):
#         match_score = 0
#         total_checks = 0

#         # 1. Full Name - Exact/Partial Match
#         if missing_person.full_name and UnidentifiedBody.full_name:
#             total_checks += 1
#             if missing_person.full_name.lower() == UnidentifiedBody.full_name.lower():
#                 match_score += 1  # Exact match
#             elif missing_person.full_name.lower() in UnidentifiedBody.full_name.lower() or UnidentifiedBody.full_name.lower() in missing_person.full_name.lower():
#                 match_score += 0.5  # Partial match

#         # 2. Age - Approximate Match
#         if missing_person.age is not None and UnidentifiedBody.estimated_age is not None:
#             total_checks += 1
#             if abs(missing_person.age - UnidentifiedBody.estimated_age) <= 5:  # Allow age range ±5
#                 match_score += 1

#         # 3. Gender - Exact Match
        # if missing_person.gender and UnidentifiedBody.gender:
        #     total_checks += 1
        #     if missing_person.gender == UnidentifiedBody.gender:
        #         match_score += 1

        # # 4. Height - Approximate Match
        # if missing_person.height and UnidentifiedBody.height:
        #     total_checks += 1
        #     if abs(missing_person.height - UnidentifiedBody.height) <= 5:  # Allow height range ±5 cm
        #         match_score += 1

        # # 5. Weight - Approximate Match
        # if missing_person.weight and UnidentifiedBody.weight:
        #     total_checks += 1
        #     if abs(missing_person.weight - UnidentifiedBody.weight) <= 5:  # Allow weight range ±5 kg
        #         match_score += 1

        # # 6. Complexion - Exact Match
        # if missing_person.complexion and UnidentifiedBody.complexion:
        #     total_checks += 1
        #     if missing_person.complexion.lower() == UnidentifiedBody.complexion.lower():
        #         match_score += 1

        # # 7. Hair Color - Exact Match
        # if missing_person.hair_color and UnidentifiedBody.hair_color:
        #     total_checks += 1
        #     if missing_person.hair_color.lower() == UnidentifiedBody.hair_color.lower():
        #         match_score += 1

        # # 8. Hair Type - Exact Match
        # if missing_person.hair_type and UnidentifiedBody.hair_type:
        #     total_checks += 1
        #     if missing_person.hair_type.lower() == UnidentifiedBody.hair_type.lower():
        #         match_score += 1

        # # 9. Eye Color - Exact Match
        # if missing_person.eye_color and UnidentifiedBody.eye_color:
        #     total_checks += 1
        #     if missing_person.eye_color.lower() == UnidentifiedBody.eye_color.lower():
        #         match_score += 1

        # # 10. Birth Mark - Exact Match
        # if missing_person.birth_mark and UnidentifiedBody.birth_mark:
        #     total_checks += 1
        #     if missing_person.birth_mark.lower() == UnidentifiedBody.birth_mark.lower():
        #         match_score += 1

        # # 11. Other Distinctive Marks - Exact Match
        # if missing_person.distinctive_mark and UnidentifiedBody.other_distinctive_mark:
        #     total_checks += 1
        #     if missing_person.distinctive_mark.lower() == UnidentifiedBody.other_distinctive_mark.lower():
        #         match_score += 1

        # # 12. Last Location of Missing Person vs Location Found - Geographic Proximity
        # if missing_person.last_seen_location and UnidentifiedBody.last_seen_details:
        #     total_checks += 1
        #     if missing_person.last_seen_location.lower() == UnidentifiedBody.last_seen_details.lower():
        #         match_score += 1


        # # 14. Photo Upload - Visual Match (optional, requires external visual comparison)
        # if missing_person.photo_upload and UnidentifiedBody.body_photo_upload:
        #     total_checks += 1
        #     if missing_person.photo_upload == UnidentifiedBody.body_photo_upload:
        #         match_score += 1    

        # # Match percentage
        # match_percentage = (match_score / total_checks) * 100 if total_checks > 0 else 0
        # return match_percentage >= 60, match_percentage




# api to confirm the persons by reporting person
class ConfirmMatchView(APIView):
    
    def post(self, request):
        missing_person_name = request.data.get('missing_person_name')
        unidentified_body_id = request.data.get('unidentified_body_id')
        unidentified_person_id = request.data.get('unidentified_person_id')
        confirmed_by = request.data.get('confirmed_by')
        relationship_with_victim = request.data.get('relationship_with_victim')  # New field
        # Validate that only one identifier is provided
        if (unidentified_body_id and unidentified_person_id) or (not unidentified_body_id and not unidentified_person_id):
            return Response(
                {'message': 'Please provide either unidentified_body_id or unidentified_person_id, not both or neither.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Find the missing person by name
        try:
            missing_person = MissingPerson.objects.get(full_name=missing_person_name, is_deleted=False)
        except MissingPerson.DoesNotExist:
            return Response({'message': 'Missing person not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the ResolvedCase record and initialize match_type
        resolved_case = ResolvedCase(missing_person=missing_person, confirmed_by=confirmed_by)
        relationship_with_victim=relationship_with_victim  
        match_type = None

        # Check if matching with an unidentified body
        if unidentified_body_id:
            try:
                unidentified_body = UnidentifiedBody.objects.get(id=unidentified_body_id, is_deleted=False)
                resolved_case.unidentified_body = unidentified_body
                match_type = 'unidentified_body'
                unidentified_body.is_deleted = True
                unidentified_body.save()
            except UnidentifiedBody.DoesNotExist:
                return Response({'message': 'Unidentified body not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if matching with an unidentified missing person
        elif unidentified_person_id:
            try:
                unidentified_missing_person = UnidentifiedMissingPerson.objects.get(id=unidentified_person_id, is_deleted=False)
                resolved_case.unidentified_missing_person = unidentified_missing_person
                match_type = 'unidentified_missing_person'
                unidentified_missing_person.delete()
                unidentified_missing_person.is_deleted = True
                unidentified_missing_person.save()
            except UnidentifiedMissingPerson.DoesNotExist:
                return Response({'message': 'Unidentified missing person not found'}, status=status.HTTP_404_NOT_FOUND)

        resolved_case.save()
            
        missing_person.is_deleted = True
        missing_person.save()
        
        matched_record = MatchedRecord(missing_person=missing_person,
                                       unidentified_body=unidentified_body if match_type == 'unidentified_body' else None,unidentified_missing_person=unidentified_missing_person if match_type == 'unidentified_missing_person' else None,
                                       confirmed_by=confirmed_by,is_deleted=False)  # New match, so we keep it active
        matched_record.save()
        response_data = {
            'message': 'Match confirmed',
            'resolved_case': {
                'missing_person_name': missing_person.full_name,
                'confirmed_by': confirmed_by,
                'relationship_with_victim':relationship_with_victim,
                'unidentified_person_name':(
                    unidentified_body.full_name if match_type == 'unidentified_body'
                    else unidentified_missing_person.full_name
                )
            },
            'matched_record':{
                'missing_person_id': matched_record.missing_person.id,
                'missing_person_name': matched_record.missing_person.full_name,
                'unidentified_body_id': matched_record.unidentified_body.id if matched_record.unidentified_body else None,
                # 'unidentified_person_id': matched_record.unidentified_missing_person.id if matched_record.unidentified_missing_person else None,
                'confirmed_by': matched_record.confirmed_by,
                'confirmation_date': matched_record.confirmation_date,
            },       
        }
        return Response(response_data, status=status.HTTP_200_OK)

# api to close the case
class CaseReportView(APIView):
    def get(self, request):
        report_data = []
        existing_report_data = []  

        # Fetch the resolved cases with related fields
        resolved_cases = ResolvedCase.objects.select_related(
            'missing_person', 'unidentified_missing_person', 'unidentified_body', 
            'unidentified_body__hospital', 'unidentified_body__police_station_name_and_address'
        )

        for case in resolved_cases:
            # Define a unique identifier for this report (e.g., report number or combination of case fields)
            report_identifier = f"{case.report_number}-{case.missing_person.id if case.missing_person else 'N/A'}"

            # Check if a report for this case already exists in the database
            existing_report = CaseReport.objects.filter(
                report_number=case.report_number, 
                case_id=f"MP-{case.missing_person.id:03}" if case.missing_person else "N/A"
            ).first()

            if existing_report:
                existing_report_data.append(CaseReportSerializer(existing_report).data)
                continue  
           
            case_entry = {
                "report_number": case.report_number,
                "case_id": f"MP-{case.missing_person.id:03}" if case.missing_person else "N/A",
                "missing_person_name": case.missing_person.full_name if case.missing_person else "N/A",  
                "status": "Resolved",
                "date_reported": case.missing_person.missing_date if case.missing_person else None,
                "reported_by": case.confirmed_by,
                "age": case.missing_person.age if case.missing_person else None,
                "gender": case.missing_person.gender if case.missing_person else "N/A",
                "last_known_location": case.missing_person.last_seen_location if case.missing_person else "N/A",
                "fir_number": case.missing_person.fir_number if case.missing_person else "N/A",
                "police_station": case.missing_person.police_station_name_and_address if case.missing_person else None,
                "police_officer_assigned": case.missing_person.investigating_officer_name if case.missing_person else "N/A",
                "case_duration": (datetime.now().date() - case.missing_person.missing_date).days if case.missing_person and case.missing_person.missing_date else None,
                "resolution_summary": "",  
                "matching_fields": "Full Name, Physical Traits, DNA",
                "closure_process": "Family notified, case closed.",
                "match_type": "",
            }

            # Match Type and related PKs
            if case.missing_person and case.unidentified_body:
                case_entry["resolution_summary"] = "Matched with UDB (Unidentified Body) found."
                case_entry["legal_and_police_involvement"] = (
                    "Police initiated investigation after body identification, forensic details provided. "
                    "Police coordinated with NGOs for identification of missing person."
                )
                case_entry["hospital_and_forensic_involvement"] = (
                    f"{case.unidentified_body.hospital.pk if case.unidentified_body.hospital else 'N/A'} "
                    f"(DNA confirmed match for UDB), and Missing Person identification using physical traits and DNA."
                )
                case_entry["match_type"] = "Unidentified Missing Person & Unidentified Dead Body"
                case_entry["missing_person_pk"] = case.missing_person.pk if case.missing_person else None 
                case_entry["unidentified_body_pk"] = case.unidentified_body.pk if case.unidentified_body else None  
                case_entry["hospital_pk"] = case.unidentified_body.hospital.pk if case.unidentified_body.hospital else None  # Ensure hospital_pk is set
                
            elif case.unidentified_body:
                case_entry["resolution_summary"] = "Matched with UDB (Unidentified Body) found."
                case_entry["legal_and_police_involvement"] = "Police initiated investigation after body identification, forensic details provided."
                # case_entry["hospital_pk"] = case.unidentified_body.hospital.pk if case.unidentified_body.hospital else None
                case_entry["hospital_and_forensic_involvement"] = (
                    f"{case.unidentified_body.hospital.pk if case.unidentified_body.hospital else 'N/A'}, "
                    f"{case.unidentified_body.police_station_name_and_address.pk if case.unidentified_body.police_station_name_and_address else 'N/A'}"
                )
                case_entry["match_type"] = "Unidentified Dead Body"
                case_entry["unidentified_body_pk"] = case.unidentified_body.pk if case.unidentified_body else None  
                case_entry["hospital_pk"] = case.unidentified_body.hospital.pk if case.unidentified_body.hospital else None  # Ensure hospital_pk is set
                
            elif case.unidentified_missing_person:
                case_entry["resolution_summary"] = "Matched with UMP (Unidentified Missing Person) found."
                case_entry["legal_and_police_involvement"] = "Police coordinated with NGOs for identification of missing person."
                case_entry["hospital_and_forensic_involvement"] = "Not Involved"
                case_entry["match_type"] = "Unidentified Missing Person"
                case_entry["hospital_pk"] = case.unidentified_body.hospital.pk if case.unidentified_body.hospital else None
                case_entry["unidentified_missing_person_pk"] = case.unidentified_missing_person.pk if case.unidentified_missing_person else None  # Store pk value
                case_entry["missing_person_pk"] = case.missing_person.pk if case.missing_person else None 
                # Since there's no `hospital` associated with `unidentified_missing_person`, no need to set hospital_pk here
                case_entry["hospital_pk"] = 1

            # Now create the CaseReport object with the correct field names
            case_report = CaseReport.objects.create(**case_entry)
            report_data.append(CaseReportSerializer(case_report).data)

        return Response({
            "report_data": report_data,
            "existing_reports": existing_report_data,
            "message": "Report generated successfully"
        }, status=status.HTTP_200_OK)


# APi for the hospital entity
class ZoneAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                zone = Zone.objects.get(pk=pk)
                serializer = ZoneSerializer(zone)
                return Response(serializer.data)
            except Zone.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        zones = Zone.objects.all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            zone = Zone.objects.get(pk=pk)
        except Zone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ZoneSerializer(zone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            zone = Zone.objects.get(pk=pk)
            zone.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Zone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class DivisionAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                division = Division.objects.get(pk=pk)
                serializer = PoliceStationNestedSerializer(division)
                return Response(serializer.data)
            except Division.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        divisions = Division.objects.all()
        serializer = DivisionNestedSerializer(divisions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DivisionNestedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            division = Division.objects.get(pk=pk)
        except Division.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = DivisionNestedSerializer(division, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            division = Division.objects.get(pk=pk)
            division.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Division.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PoliceStationAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                police_station = PoliceStation.objects.get(pk=pk)
                serializer = PoliceStationNestedSerializer(police_station)
                return Response(serializer.data)
            except PoliceStation.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        police_stations = PoliceStation.objects.all()
        serializer = PoliceStationNestedSerializer(police_stations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PoliceStationNestedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            police_station = PoliceStation.objects.get(pk=pk)
        except PoliceStation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PoliceStationNestedSerializer(police_station, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            police_station = PoliceStation.objects.get(pk=pk)
            police_station.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PoliceStation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ChowkiAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                chowki = Chowki.objects.get(pk=pk)
                serializer = ChowkiSerializer(chowki)
                return Response(serializer.data)
            except Chowki.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        chowkis = Chowki.objects.all()
        serializer = ChowkiSerializer(chowkis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChowkiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            chowki = Chowki.objects.get(pk=pk)
        except Chowki.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChowkiSerializer(chowki, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            chowki = Chowki.objects.get(pk=pk)
            chowki.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Chowki.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# api for hospital entity
class HospitalZoneAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                zone = HospitalZone.objects.get(pk=pk)
                serializer = HospitalZoneSerializer(zone)
                return Response(serializer.data)
            except HospitalZone.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        zones = HospitalZone.objects.all()
        serializer = HospitalZoneSerializer(zones, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalZoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            zone = HospitalZone.objects.get(pk=pk)
        except HospitalZone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalZoneSerializer(zone, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            zone = HospitalZone.objects.get(pk=pk)
            zone.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HospitalZone.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class HospitalDivisionAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                division = HospitalDivision.objects.get(pk=pk)
                serializer = HospitalDivisionSerializer(division)
                return Response(serializer.data)
            except HospitalDivision.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        divisions = HospitalDivision.objects.all()
        serializer = HospitalDivisionSerializer(divisions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalDivisionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            division = HospitalDivision.objects.get(pk=pk)
        except HospitalDivision.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalDivisionSerializer(division, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            division = HospitalDivision.objects.get(pk=pk)
            division.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HospitalDivision.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class HospitalAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                hospital = Hospital.objects.get(pk=pk)
                serializer = HospitalSerializer(hospital)
                return Response(serializer.data)
            except Hospital.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            hospital = Hospital.objects.get(pk=pk)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HospitalSerializer(hospital, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            hospital = Hospital.objects.get(pk=pk)
            hospital.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Hospital.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



# class MatchMissingPersonWithBodyAPIView(APIView):
#     def post(self, request):
#         missing_person_id = request.data.get('missing_person_id')
#         unidentified_body_id = request.data.get('unidentified_body_id')
        
#         try:
#             missing_person = MissingPerson.objects.get(id=missing_person_id, is_deleted=False)
#             unidentified_body = UnidentifiedBody.objects.get(id=unidentified_body_id, is_deleted=False)
            
#             matched_record = MatchedRecord.objects.create(
#                 missing_person=missing_person,
#                 unidentified_body=unidentified_body,
#                 confirmed_by=request.get('confirmed_by')
#             )
            
#             return Response({'message': 'Match created successfully', 'match_id': matched_record.id}, status=status.HTTP_201_CREATED)
        
#         except MissingPerson.DoesNotExist:
#             return Response({'error': 'Missing person not found'}, status=status.HTTP_404_NOT_FOUND)
#         except UnidentifiedBody.DoesNotExist:
#             return Response({'error': 'Unidentified body not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class MatchMissingPersonWithUnidentifiedPersonAPIView(APIView):
#     def post(self, request):
#         missing_person_id = request.data.get('missing_person_id')
#         unidentified_missing_person_id = request.data.get('unidentified_missing_person_id')
        
#         try:
#             missing_person = MissingPerson.objects.get(id=missing_person_id, is_deleted=False)
#             unidentified_missing_person = UnidentifiedMissingPerson.objects.get(id=unidentified_missing_person_id, is_deleted=False)
            
#             matched_record = MatchedRecord.objects.create(
#                 missing_person=missing_person,
#                 unidentified_missing_person=unidentified_missing_person,
#                 confirmed_by=request.get('confirmed_by')
#             )
            
#             return Response({'message': 'Match created successfully', 'match_id': matched_record.id}, status=status.HTTP_201_CREATED)
        
#         except MissingPerson.DoesNotExist:
#             return Response({'error': 'Missing person not found'}, status=status.HTTP_404_NOT_FOUND)
#         except UnidentifiedMissingPerson.DoesNotExist:
#             return Response({'error': 'Unidentified missing person not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
