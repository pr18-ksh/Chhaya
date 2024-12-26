from django.urls import path
from .views import CaseReportView, ChowkiAPIView, ConfirmMatchView, DivisionAPIView, HospitalAPIView, HospitalDivisionAPIView, HospitalZoneAPIView,MissingPersonAPIView, PoliceStationAPIView, RejectMatchAPIView,SearchIndividualMatches, UnidentifiedBodyAPIView, UnidentifiedMissingperson, VolunteerAPIView, ZoneAPIView


urlpatterns = [
    
    # url for missing person
    path('missing-person/', MissingPersonAPIView.as_view(), name='missing_person_list'),
    path('missing-person/<int:missing_person_id>/', MissingPersonAPIView.as_view(), name='missing_person_detail'),
    
    # url for the unidentified missing person
    path('undefined-missing-persons/', UnidentifiedMissingperson.as_view(), name='undefined_missing_persons'),
    path('undefined-missing-persons/<int:undefined_missing_person_id>/', UnidentifiedMissingperson.as_view(), name='undefined_missing_person_detail'),
    
    # url for the unidentified dead body
    path('unidentified-bodies/', UnidentifiedBodyAPIView.as_view(), name='unidentified-body-list'),
    path('unidentified-bodies/<int:unidentified_body_id>/', UnidentifiedBodyAPIView.as_view(), name='unidentified-body-detail'),
    
    # url for the volunteer
    path('volunteer/', VolunteerAPIView.as_view(), name='volunteer-list'),
    path('volunteer/<int:volunteer_id>/', VolunteerAPIView.as_view(), name='volunteer-detail'),
    
    # url for the match data between two persons
    # path('search-all-matches/', SearchAllMatches.as_view(), name='search_all_matches'),
      path('search-all-matches/', SearchIndividualMatches.as_view(), name='search_all_matches'),
      
    # url for the confirm data after match the data
    path('confirm_match/', ConfirmMatchView.as_view(), name='confirm-match'),
    
    # url to generate the report
    path('report/', CaseReportView.as_view(), name='case_report'),
    
    # this urls for the police stations 
    path('police-zones/', ZoneAPIView.as_view(), name='zone-list-create'),  
    path('police-zones/<int:pk>/', ZoneAPIView.as_view(), name='zone-detail'),  
    path('police-divisions/', DivisionAPIView.as_view(), name='division-list-create'),  
    path('police-divisions/<int:pk>/', DivisionAPIView.as_view(), name='division-detail'),  
    path('police-stations/', PoliceStationAPIView.as_view(), name='police-station-list-create'), 
    path('police-stations/<int:pk>/', PoliceStationAPIView.as_view(), name='police-station-detail'),   
    path('police-chowkis/', ChowkiAPIView.as_view(), name='chowki-list-create'),  
    path('police-chowkis/<int:pk>/', ChowkiAPIView.as_view(), name='chowki-detail'), 
    
    # this api for the hospitals 
    path('hospital-zones/', HospitalZoneAPIView.as_view(), name='hospital-zone-list'),  
    path('hospital-zones/<int:pk>/', HospitalZoneAPIView.as_view(), name='hospital-zone-detail'),  
    path('hospital-divisions/', HospitalDivisionAPIView.as_view(), name='hospital-division-list'),  
    path('hospital-divisions/<int:pk>/', HospitalDivisionAPIView.as_view(), name='hospital-division-detail'),
    path('hospitals/', HospitalAPIView.as_view(), name='hospital-list'), 
    path('hospitals/<int:pk>/', HospitalAPIView.as_view(), name='hospital-detail'),
    path('reject/', RejectMatchAPIView.as_view(), name='reject-match'), 
   
#     path('match-missing-person-with-body/', MatchMissingPersonWithBodyAPIView.as_view(), name='match-missing-person-with-body'),
    
#     # URL for matching missing person with unidentified missing person
#     path('match-missing-person-with-unidentified-person/', MatchMissingPersonWithUnidentifiedPersonAPIView.as_view(), name='match-missing-person-with-unidentified-person'),
    
]