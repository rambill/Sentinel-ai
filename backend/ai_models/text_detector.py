"""
AI-Powered Text Analysis Module
Detects: Phishing, Scams, AI-generated text, Spam
"""
import re
import nltk
from textblob import TextBlob
from langdetect import detect, LangDetectException
from typing import Dict, List, Tuple
import validators
import tldextract

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


class TextScamDetector:
    """Advanced text analysis for scam and phishing detection"""
    
    def __init__(self):
        # Phishing/Scam indicators
        self.urgency_keywords = [
            'urgent', 'immediately', 'act now', 'limited time', 'expires',
            'hurry', 'quick', 'fast', 'asap', 'right now', 'don\'t wait',
            'last chance', 'final notice', 'time sensitive', 'act fast',
            'don\'t delay', 'respond now', 'within 24 hours', 'within 48 hours',
            'today only', 'expires today', 'expires soon', 'limited offer',
            'ending soon', 'while supplies last', 'before it\'s too late',
            'don\'t miss', 'act immediately', 'respond immediately'
        ]
        
        self.threat_keywords = [
            'suspended', 'locked', 'blocked', 'terminated', 'closed',
            'unauthorized', 'unusual activity', 'security alert', 'verify',
            'confirm', 'update', 'validate', 'compromised', 'breach',
            'fraud', 'fraudulent', 'suspicious', 'detected', 'warning',
            'alert', 'critical', 'action required', 'immediate action',
            'account suspended', 'account locked', 'access denied',
            'security breach', 'data breach', 'hacked', 'virus detected',
            'malware detected', 'unauthorized access', 'suspicious login',
            'verify identity', 'confirm identity', 'update required',
            'verification required', 'action needed', 'must verify'
        ]
        
        self.financial_keywords = [
            'bank', 'account', 'credit card', 'payment', 'refund', 'prize',
            'winner', 'lottery', 'inheritance', 'money', 'cash', 'transfer',
            'wire', 'bitcoin', 'cryptocurrency', 'investment', 'claim',
            'reward', 'bonus', 'free money', 'million', 'thousand', 'dollars',
            'processing fee', 'transaction', 'deposit', 'withdraw',
            'paypal', 'venmo', 'zelle', 'cashapp', 'western union',
            'gift card', 'amazon card', 'itunes card', 'google play card',
            'tax refund', 'irs', 'social security', 'stimulus check',
            'unclaimed funds', 'inheritance claim', 'lottery winnings',
            'you won', 'congratulations winner', 'claim prize', 'claim reward',
            # Ugandan-specific financial terms
            'mobile money', 'mtn money', 'airtel money', 'momo', 'send airtime',
            'shillings', 'ugx', 'ush', 'boda boda', 'mpesa', 'm-pesa',
            'centenary bank', 'stanbic', 'dfcu', 'equity bank', 'bank of uganda',
            'nssf', 'ura', 'umeme', 'nwsc', 'kcca', 'kampala', 'entebbe'
        ]
        
        self.action_keywords = [
            'click here', 'click link', 'download', 'open attachment',
            'reply', 'call now', 'contact us', 'verify account', 'reset password',
            'update information', 'confirm identity', 'provide details',
            'send', 'give us', 'share your', 'enter your', 'submit',
            'fill out', 'complete', 'respond', 'act now',
            'click below', 'tap here', 'follow link', 'visit link',
            'go to', 'login here', 'sign in here', 'update here',
            'verify here', 'confirm here', 'download now', 'install now',
            # Ugandan-specific action phrases
            'dial', 'send to', 'flash', 'call back', 'sms to', 'text to'
        ]
        
        # Ugandan-specific scam patterns
        self.ugandan_scam_patterns = [
            # Mobile money scams
            r'\b(mtn|airtel)\s+(money|momo)\s+(pin|password|code)\b',
            r'\bsend\s+\d+\s+(shillings|ugx|ush)\b',
            r'\b(won|win|winner)\s+.*(mtn|airtel|uganda)\b',
            # Government impersonation
            r'\b(ura|nssf|kcca|umeme|nwsc)\s+(refund|payment|fine|penalty)\b',
            # Common Ugandan phone scams
            r'\b(flash|missed\s+call|call\s+back)\s+.*(win|prize|reward)\b',
            # Fake job offers
            r'\b(job|employment|vacancy)\s+.*(urgent|immediate|no\s+experience)\b',
            # Fake loan offers
            r'\b(loan|credit|borrow)\s+.*(instant|quick|no\s+collateral)\b',
        ]
        
        self.suspicious_domains = [
            'bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'is.gd',
            'buff.ly', 'adf.ly', 'short.link', 'tiny.cc', 'rb.gy'
        ]
        
        # AI-generated text patterns
        self.ai_patterns = [
            r'\b(as an ai|i am an ai|i\'m an ai|language model)\b',
            r'\b(i don\'t have personal|i cannot|i\'m unable to)\b',
            r'\b(it\'s important to note|it\'s worth noting)\b',
            r'\b(in conclusion|to summarize|in summary)\b',
            r'\b(various|numerous|multitude of|plethora)\b',
        ]
    
    def analyze(self, text: str) -> Dict:
        """Main analysis function"""
        if not text or len(text.strip()) < 10:
            return self._create_response(False, 50, "low", 
                                        "Text too short for analysis",
                                        ["Insufficient text length"])
        
        # Run all detection methods
        urgency_score = self._detect_urgency(text)
        threat_score = self._detect_threats(text)
        financial_score = self._detect_financial_lures(text)
        action_score = self._detect_suspicious_actions(text)
        url_score = self._analyze_urls(text)
        grammar_score = self._analyze_grammar(text)
        ai_score = self._detect_ai_generated(text)
        sentiment_score = self._analyze_sentiment(text)
        impersonation_score = self._detect_impersonation(text)
        ugandan_scam_score = self._detect_ugandan_scams(text)
        
        # Calculate overall scam probability
        total_score = (
            urgency_score * 2.0 +      
            threat_score * 2.5 +       
            financial_score * 2.2 +    
            action_score * 2.0 +       
            url_score * 3.0 +          
            grammar_score * 1.5 +      
            ai_score * 1.0 +
            impersonation_score * 2.5 +
            ugandan_scam_score * 2.8  # High weight for local scams
        )
        
        # Normalize to 0-100 with better scaling
        confidence = min(int(total_score * 8), 99)  # Changed from * 10
        is_scam = confidence >= 50  # Lowered from 60
        
        # Determine threat level
        if confidence >= 70:  # Lowered from 80
            threat_level = "high"
        elif confidence >= 40:  # Lowered from 50
            threat_level = "medium"
        else:
            threat_level = "low"
        
        # Generate explanation
        explanation = self._generate_explanation(
            is_scam, confidence, urgency_score, threat_score,
            financial_score, url_score, ai_score
        )
        
        # Collect indicators
        indicators = self._collect_indicators(
            urgency_score, threat_score, financial_score,
            action_score, url_score, grammar_score, ai_score
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(is_scam, threat_level)
        
        return self._create_response(
            is_scam, confidence, threat_level,
            explanation, indicators, recommendation
        )
    
    def _detect_urgency(self, text: str) -> float:
        """Detect urgency tactics"""
        text_lower = text.lower()
        count = sum(1 for keyword in self.urgency_keywords if keyword in text_lower)
        return min(count * 0.8, 5.0)
    
    def _detect_threats(self, text: str) -> float:
        """Detect threat language"""
        text_lower = text.lower()
        count = sum(1 for keyword in self.threat_keywords if keyword in text_lower)
        return min(count * 1.0, 5.0)
    
    def _detect_financial_lures(self, text: str) -> float:
        """Detect financial incentives/threats"""
        text_lower = text.lower()
        count = sum(1 for keyword in self.financial_keywords if keyword in text_lower)
        return min(count * 0.9, 5.0)
    
    def _detect_suspicious_actions(self, text: str) -> float:
        """Detect requests for action"""
        text_lower = text.lower()
        count = sum(1 for keyword in self.action_keywords if keyword in text_lower)
        return min(count * 1.0, 5.0)
    
    def _analyze_urls(self, text: str) -> float:
        """Analyze URLs in text"""
        score = 0.0
        
        # Find URLs with http/https
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        # Also find URLs without protocol (bit.ly, tinyurl.com, etc.)
        domain_pattern = r'\b(?:bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|adf\.ly|short\.link)/[a-zA-Z0-9]+'
        urls.extend(re.findall(domain_pattern, text))
        
        # Find suspicious TLDs even without full URL
        tld_pattern = r'\b\w+\.(?:tk|ml|ga|cf|gq|xyz|top)\b'
        suspicious_tlds = re.findall(tld_pattern, text)
        if suspicious_tlds:
            score += 2.5 * len(suspicious_tlds)
        
        if not urls and not suspicious_tlds:
            return 0.0
        
        for url in urls:
            # Check for URL shorteners
            if any(short in url.lower() for short in self.suspicious_domains):
                score += 3.0  # Increased from 2.5
            
            # Check for suspicious TLDs in full URLs
            suspicious_tlds_list = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
            if any(url.endswith(tld) for tld in suspicious_tlds_list):
                score += 2.5  # Increased from 2.0
            
            # Check for IP addresses in URL
            if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                score += 3.0  # Increased from 2.5
            
            # Check for lookalike domains (common in phishing)
            lookalike_patterns = [
                r'paypa1', r'g00gle', r'micr0soft', r'amaz0n', r'app1e',
                r'faceb00k', r'netf1ix', r'bank-', r'-secure', r'-verify',
                r'-update', r'-login', r'-account'
            ]
            if any(re.search(pattern, url.lower()) for pattern in lookalike_patterns):
                score += 2.5
        
        return min(score, 5.0)
    
    def _analyze_grammar(self, text: str) -> float:
        """Analyze grammar and spelling quality"""
        try:
            blob = TextBlob(text)
            
            # Check spelling errors
            words = blob.words
            if len(words) == 0:
                return 0.0
            
            # Filter out common informal words and contractions that aren't misspellings
            informal_words = {
                'hey', 'gonna', 'wanna', 'gotta', 'yeah', 'yep', 'nope', 
                'ok', 'okay', 'btw', 'lol', 'omg', 'thx', 'pls', 'ur',
                'shoulda', 'coulda', 'woulda', 'kinda', 'sorta'
            }
            
            # Also ignore proper nouns and short words
            misspelled = 0
            for word in words:
                word_lower = word.lower()
                # Skip if: informal word, proper noun (capitalized), or very short
                if (word_lower in informal_words or 
                    word[0].isupper() or 
                    len(word) <= 2):
                    continue
                
                corrected = word.correct()
                if word_lower != corrected.lower():
                    misspelled += 1
            
            error_rate = misspelled / len(words) if len(words) > 0 else 0
            
            # Poor grammar often indicates scams (but be very lenient with casual messages)
            if error_rate > 0.25:  # Very high threshold - only flag obvious issues
                return 3.0
            elif error_rate > 0.15:  # High threshold
                return 1.5
            
            return 0.0
        except:
            return 0.0
    
    def _detect_ai_generated(self, text: str) -> float:
        """Detect AI-generated text patterns"""
        text_lower = text.lower()
        score = 0.0
        
        # Check for AI patterns
        for pattern in self.ai_patterns:
            if re.search(pattern, text_lower):
                score += 1.0
        
        # Check for overly formal/perfect structure
        sentences = sent_tokenize(text)
        if len(sentences) > 3:
            avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
            # AI tends to generate consistent sentence lengths
            if 15 <= avg_length <= 25:
                score += 0.5
        
        return min(score, 3.0)
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment (fear, urgency)"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            # Negative sentiment often in scams
            if polarity < -0.3:
                return 1.5
            
            return 0.0
        except:
            return 0.0
    
    def _detect_impersonation(self, text: str) -> float:
        """Detect impersonation of legitimate organizations"""
        text_lower = text.lower()
        score = 0.0
        
        # Common impersonated organizations
        organizations = [
            'amazon', 'paypal', 'netflix', 'microsoft', 'apple', 'google',
            'facebook', 'instagram', 'twitter', 'bank of america', 'chase',
            'wells fargo', 'irs', 'social security', 'fedex', 'ups', 'dhl',
            'ebay', 'walmart', 'target', 'best buy', 'geek squad',
            # Ugandan organizations
            'mtn', 'airtel', 'centenary bank', 'stanbic', 'dfcu', 'equity bank',
            'bank of uganda', 'ura', 'nssf', 'kcca', 'umeme', 'nwsc'
        ]
        
        # Check if message claims to be from these organizations
        for org in organizations:
            if org in text_lower:
                # Higher score if combined with threat/urgency
                if any(keyword in text_lower for keyword in ['suspended', 'locked', 'verify', 'confirm', 'urgent', 'winner', 'won']):
                    score += 2.0
                else:
                    score += 0.5
        
        # Check for "from" or "team" patterns
        impersonation_patterns = [
            r'\bfrom\s+(?:amazon|paypal|netflix|microsoft|apple|google|bank|mtn|airtel)\b',
            r'\b(?:amazon|paypal|netflix|microsoft|apple|google|bank|mtn|airtel)\s+team\b',
            r'\b(?:amazon|paypal|netflix|microsoft|apple|google|bank|mtn|airtel)\s+support\b',
            r'\bofficial\s+(?:amazon|paypal|netflix|microsoft|apple|google|bank|mtn|airtel)\b'
        ]
        
        for pattern in impersonation_patterns:
            if re.search(pattern, text_lower):
                score += 1.5
        
        return min(score, 5.0)
    
    def _detect_ugandan_scams(self, text: str) -> float:
        """Detect Uganda-specific scam patterns"""
        text_lower = text.lower()
        score = 0.0
        
        # Check for Ugandan scam patterns
        for pattern in self.ugandan_scam_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 2.0
        
        # Mobile money scams
        if any(term in text_lower for term in ['mtn money', 'airtel money', 'mobile money', 'momo']):
            if any(term in text_lower for term in ['pin', 'password', 'code', 'verify', 'confirm']):
                score += 2.5
        
        # Prize/lottery scams with Ugandan context
        if any(term in text_lower for term in ['won', 'winner', 'prize', 'reward']):
            if any(term in text_lower for term in ['mtn', 'airtel', 'uganda', 'kampala']):
                score += 2.0
        
        # Fake government communications
        if any(term in text_lower for term in ['ura', 'nssf', 'kcca', 'umeme', 'nwsc']):
            if any(term in text_lower for term in ['refund', 'fine', 'penalty', 'payment', 'urgent']):
                score += 2.5
        
        # Flash/callback scams (very common in Uganda)
        if any(term in text_lower for term in ['flash', 'missed call', 'call back', 'dial']):
            if any(term in text_lower for term in ['win', 'prize', 'reward', 'free']):
                score += 2.0
        
        return min(score, 5.0)
    
    def _generate_explanation(self, is_scam: bool, confidence: int,
                            urgency: float, threat: float, financial: float,
                            url: float, ai: float) -> str:
        """Generate human-readable explanation"""
        if is_scam:
            reasons = []
            if urgency > 1.0:
                reasons.append("urgency tactics")
            if threat > 1.0:
                reasons.append("threatening language")
            if financial > 1.0:
                reasons.append("financial incentives")
            if url > 1.0:
                reasons.append("suspicious URLs")
            if ai > 1.0:
                reasons.append("AI-generated patterns")
            
            reason_text = ", ".join(reasons) if reasons else "multiple red flags"
            
            return (f"This message exhibits characteristics of a phishing/scam attempt "
                   f"with {confidence}% confidence. Our AI detected {reason_text}. "
                   f"The content uses manipulation tactics commonly found in fraudulent communications.")
        else:
            # For legitimate messages, show the scam confidence (which is low)
            return (f"This message appears legitimate. Our AI found only {confidence}% "
                   f"scam indicators, which is below the threshold for concern. "
                   f"The content follows standard communication patterns with appropriate language and structure.")
    
    def _collect_indicators(self, urgency: float, threat: float, financial: float,
                          action: float, url: float, grammar: float, ai: float) -> List[str]:
        """Collect detected indicators"""
        indicators = []
        
        if urgency > 1.0:
            indicators.append("⚠️ Uses urgency and pressure tactics")
        if threat > 1.0:
            indicators.append("⚠️ Contains threatening or alarming language")
        if financial > 1.0:
            indicators.append("⚠️ Mentions financial incentives or threats")
        if action > 1.0:
            indicators.append("⚠️ Requests immediate action or personal information")
        if url > 2.0:
            indicators.append("⚠️ Contains suspicious or shortened URLs")
        elif url > 0.5:
            indicators.append("⚠️ Contains URLs (verify before clicking)")
        if grammar > 1.5:
            indicators.append("⚠️ Poor grammar and spelling detected")
        if ai > 1.0:
            indicators.append("🤖 AI-generated text patterns detected")
        
        if not indicators:
            indicators = [
                "✅ Professional language and tone",
                "✅ No suspicious URLs detected",
                "✅ Standard communication patterns",
                "✅ Proper grammar and formatting"
            ]
        
        return indicators
    
    def _generate_recommendation(self, is_scam: bool, threat_level: str) -> str:
        """Generate actionable recommendation"""
        if is_scam:
            if threat_level == "high":
                return ("🚨 HIGH RISK: Do NOT click any links, download attachments, or provide "
                       "any information. Delete this message immediately and report it as spam. "
                       "If claiming to be from a legitimate organization, contact them directly "
                       "through official channels (not using contact info from this message).")
            elif threat_level == "medium":
                return ("⚠️ MEDIUM RISK: Exercise extreme caution. Verify the sender's identity "
                       "through official channels before taking any action. Do not click links "
                       "or provide sensitive information. When in doubt, delete the message.")
            else:
                return ("⚡ LOW RISK: While some suspicious elements detected, verify sender "
                       "authenticity before proceeding. Use official contact methods to confirm.")
        else:
            return ("✅ This message appears safe, but always verify sender identity before "
                   "sharing sensitive information or clicking links. Stay vigilant and trust "
                   "your instincts if something feels off.")
    
    def _create_response(self, is_scam: bool, confidence: int, threat_level: str,
                        explanation: str, indicators: List[str],
                        recommendation: str = None) -> Dict:
        """Create standardized response"""
        return {
            "isScam": is_scam,
            "confidence": confidence,
            "threatLevel": threat_level,
            "explanation": explanation,
            "indicators": indicators,
            "recommendation": recommendation or self._generate_recommendation(is_scam, threat_level)
        }
