# Parte del contenuto del file models.py:
class Campaign(models.Model):
    name = models.CharField(max_length=128)
    status = models.IntegerField(default=CampaignStatus.DRAFT, 
                    choices=CampaignStatus.choices)
    type = models.CharField(default=CampaignTypes.PKG, 
                    choices=CampaignTypes.choices, max_length=3)
    mode = models.CharField(default=CampaignModes.STANDARD, 
                    choices=CampaignModes.choices, max_length=3)
    id_ticket = models.CharField(max_length=16)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)
    idrs = models.CharField(max_length=32)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    algorithm_started_at = models.DateTimeField(null=True)
    algorithm_scheduling_note = models.TextField(max_length=4096, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['idrs'])
        ]


# Parte del contenuto del file views.py:
class CampaignListCreateAPIView(generics.ListCreateAPIView):
    queryset = Campaign.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['name', 'type', 'status', 'start_at',
                         'end_at', 'created_at']
    serializer_class = CampaignSerializer

    def perform_create(self, serializer):
        serializer.save(status=CampaignStatus.DRAFT, 
                created_by_id=self.request.user.id)


# Parte del contenuto del file serializers.py:
class CampaignSerializer(CampaignSerializer):
    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at',
                            'algorithm_started_at', 'algorithm_scheduling_note')


# Parte del contenuto del file urls.py:
path('campaigns/', CampaignListCreateAPIView.as_view()),
