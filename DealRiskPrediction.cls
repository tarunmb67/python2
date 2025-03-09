public with sharing class DealRiskPrediction {
    
    @InvocableMethod(label='Get Deal Risk Score' description='Calls AI API to get deal risk score')
    public static List<DealRiskResult> getDealRisk(List<DealRiskRequest> requests) {
        List<DealRiskResult> riskScores = new List<DealRiskResult>();        
        List<Id> OppIds = new List<Id>();
        DealRiskRequest req = requests[0];
        OppIds.add(req.opportunityId);
        getDealScore(OppIds);
        return riskScores;
    }
    
    @future(callout=true)
    public static void getDealScore(List<Id> opportunityId){
        List<Opportunity> listofOppstoUpdate = new List<Opportunity>();
        Opportunity opp = [SELECT Id,Amount, StageName, CloseDate, LeadSource, Probability,
                           Risk_Score__c,customer_engagement__c,Competitor_Presence__c FROM Opportunity WHERE Id =: opportunityId[0] LIMIT 1];
        String RiskScore = '';
        Decimal PredictedRiskScore = 0.0;
        String apiUrl = 'https://deal-risk-api.onrender.com/predict';
        Integer daysToClose = opp.CloseDate.daysBetween(Date.today());       
        Integer stageEncoded = encodeStage(opp.StageName);
        Integer leadSourceEncoded = encodeLeadSource(opp.LeadSource);
        
        // Prepare JSON request body
        String jsonBody = JSON.serialize(new Map<String, Object>{
            'features' => new List<Object>{
                opp.Amount, 
                    stageEncoded, 
                    daysToClose, 
                    leadSourceEncoded, 
                    0.5, 
                    1,    
                    0.75  
                    }
        });
        
        HttpRequest request = new HttpRequest();
        request.setEndpoint(apiUrl);
        request.setMethod('POST');
        request.setHeader('Content-Type', 'application/json');
        request.setBody(jsonBody);
        request.setTimeout(20000);
        
        Http http = new Http();
        HttpResponse response = http.send(request);
        
        if (response.getStatusCode() == 200) {
            Map<String, Object> responseData = (Map<String, Object>) JSON.deserializeUntyped(response.getBody());
            RiskScore = (String) responseData.get('risk_score');
            PredictedRiskScore = (Decimal) responseData.get('Predicted Deal Risk Score');
            Opportunity opp1 = new Opportunity();
            opp1.Id = opp.Id;
            opp1.Risk_Score__c = RiskScore;
            opp1.Predicted_Risk_Score__c = PredictedRiskScore;
            listofOppstoUpdate.add(opp1);
        } else {
            RiskScore = 'Error';
        }
        if(listofOppstoUpdate.size() > 0){
            Update listofOppstoUpdate;
        }
        system.debug('@@@@ RiskScore '+RiskScore);
    }
    
    // Define Input Structure for Flow
    public class DealRiskRequest {
        @InvocableVariable(label='Deal Size' required=true)
        public Decimal dealSize;
        
        @InvocableVariable(label='Customer Engagement' required=true)
        public Decimal customerEngagement;
        
        @InvocableVariable(label='Competitor Presence' required=true)
        public Integer competitorPresence;
        
        @InvocableVariable(label='Opportunity Id' required=true)
        public Id opportunityId;
    }
    
    public class DealRiskResult {
        @InvocableVariable(label='Risk Score' required=true)
        public String RiskScore;
    }
    public static Integer encodeStage(String stage) {
        Map<String, Integer> stageMap = new Map<String, Integer>{
            'Prospecting' => 1,
            'Qualification' => 2,
            'Proposal' => 3,
            'Negotiation/Review' => 4,
            'Closed Won' => 5,
            'Closed Lost' => 0
        };
        return stageMap.containsKey(stage) ? stageMap.get(stage) : -1;
    }

    // Helper function to encode lead sources
    public static Integer encodeLeadSource(String leadSource) {
        Map<String, Integer> sourceMap = new Map<String, Integer>{
            'Web' => 0,
            'Referral' => 1,
            'Cold Call' => 2,
            'Trade Show' => 3
        };
        return sourceMap.containsKey(leadSource) ? sourceMap.get(leadSource) : -1;
    }
}
