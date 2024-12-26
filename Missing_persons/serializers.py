
from rest_framework import serializers

from .models import Address, CaseReport, Chowki, Contact, Division, Hospital, HospitalDivision, HospitalZone, MatchedRecord, MissingPerson, PoliceStation, UnidentifiedBody, UnidentifiedMissingPerson, Volunteer,Match, Zone



# for the all persons serializers 
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        
class MissingPersonSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    address = AddressSerializer()
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = MissingPerson
        fields = '__all__'

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')

        # Create nested objects
        contact = Contact.objects.create(**contact_data)
        address = Address.objects.create(**address_data)

        # Create the MissingPerson instance
        missing_person = MissingPerson.objects.create(
            contact=contact,
            address=address,
            **validated_data
        )
        return missing_person

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)
        address_data = validated_data.pop('address', None)

        # Update contact and address if provided
        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()

        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        # Update the MissingPerson instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class UndefinedMissingpersonSerializer(serializers.ModelSerializer):
    address = AddressSerializer()  
    contact = ContactSerializer()  

    class Meta:
        model = UnidentifiedMissingPerson
        fields = '__all__' 

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        contact_data = validated_data.pop('contact')

        # Create Address instance
        address = Address.objects.create(**address_data)
        contact = Contact.objects.create(**contact_data)

        # Create unidentified missing person instance with the created Address and Contact
        personal_details = UnidentifiedMissingPerson.objects.create(
            address=address,
            contact=contact,
            **validated_data
        )

        return personal_details

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        contact_data = validated_data.pop('contact', None)

        # Update Address instance if address data is provided
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        # Update Contact instance if contact data is provided
        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()

        # Update other fields in PersonalDetails
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance 
    
class UnidentifiedBodySerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    address = AddressSerializer()

    class Meta:
        model = UnidentifiedBody
        fields = '__all__'

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')

        # Create the nested Contact and Address instances
        contact = Contact.objects.create(**contact_data)
        address = Address.objects.create(**address_data)

        # Create the UnidentifiedBody instance with the newly created Contact and Address
        unidentified_body = UnidentifiedBody.objects.create(
            contact=contact,
            address=address,
            **validated_data
        )

        return unidentified_body

    def update(self, instance, validated_data):
        contact_data = validated_data.pop('contact', None)
        address_data = validated_data.pop('address', None)

        # Update the nested Contact instance
        if contact_data:
            for attr, value in contact_data.items():
                setattr(instance.contact, attr, value)
            instance.contact.save()

        # Update the nested Address instance
        if address_data:
            for attr, value in address_data.items():
                setattr(instance.address, attr, value)
            instance.address.save()

        # Update the UnidentifiedBody instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
    
class VolunteerSerializer(serializers.ModelSerializer):
    # Nested serializers for contacts and addresses
    contact = ContactSerializer()
    address = AddressSerializer()

    class Meta:
        model = Volunteer
        fields = '__all__'

    def create(self, validated_data):
        # Extract nested data
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')

        # Create the contact and address first
        contact = Contact.objects.create(**contact_data)
        address = Address.objects.create(**address_data)

        # Create the volunteer with the contact and address
        volunteer = Volunteer.objects.create(contact=contact, address=address, **validated_data)
        return volunteer

    def update(self, instance, validated_data):
        # Extract nested data
        contact_data = validated_data.pop('contact')
        address_data = validated_data.pop('address')

        # Update or create contact
        contact, created = Contact.objects.update_or_create(
            id=instance.contact.id, defaults=contact_data
        )

        # Update or create address
        address, created = Address.objects.update_or_create(
            id=instance.address.id, defaults=address_data
        )

        # Update volunteer fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
      

    
    
# for the police station entity 
class MatchSerializer(serializers.ModelSerializer):
    missing_person = MissingPersonSerializer()
    undefined_missing_person = UndefinedMissingpersonSerializer(required=False)
    unidentified_body = UnidentifiedBodySerializer(required=False)
    rejection_reason = serializers.CharField(max_length=255, required=False)
    class Meta:
        model = Match
        fields = ['missing_person', 'undefined_missing_person', 'unidentified_body','rejection_reason', 'match_percentage', 'match_type']
    
class ChowkiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chowki
        fields = ['id', 'name', 'telephone_no', 'address', 'police_station']  # Include police_station if needed, else remove it

class PoliceStationNestedSerializer(serializers.ModelSerializer):
    chowkis = ChowkiSerializer(many=True, read_only=True)  # This will automatically look for chowkis based on the related_name

    class Meta:
        model = PoliceStation
        fields = ['id', 'name', 'address', 'telephone_no', 'division', 'chowkis']  # Use fields you need

class DivisionNestedSerializer(serializers.ModelSerializer):
    zone = serializers.PrimaryKeyRelatedField(read_only=True, source='zone.id')
    stations = PoliceStationNestedSerializer(many=True, read_only=True, source='police_stations')

    class Meta:
        model = Division
        fields = ['zone', 'id', 'name', 'stations']

class ZoneSerializer(serializers.ModelSerializer):
    divisions = DivisionNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Zone
        fields = ['id', 'name', 'divisions']
        
        
        
# for the hospital entity
class HospitalZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalZone
        fields = ['id', 'name']  

class HospitalDivisionSerializer(serializers.ModelSerializer):
    zone = HospitalZoneSerializer(read_only=True)

    class Meta:
        model = HospitalDivision
        fields = ['id', 'name', 'zone'] 

class HospitalSerializer(serializers.ModelSerializer):
    division = HospitalDivisionSerializer(read_only=True)

    class Meta:
        model = Hospital
        fields = ['id', 'name', 'entity_type', 'Address', 'division']



class CaseReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseReport
        fields = '__all__'
        
class MatchedRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchedRecord
        fields = '__all__'