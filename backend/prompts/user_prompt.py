"""
User prompt template for Smart Plant Health Assistant.
Contains image analysis instructions and analysis framework.
NOT to be mixed with image processing or UI logic.
"""

USER_PROMPT_TEMPLATE = """
Please analyze the provided plant image and provide a comprehensive health assessment.

Image Information:
- Dimensions: {image_width}x{image_height}
- Format: {image_format}
- Captured: {capture_timestamp}

Analysis Instructions:
1. **Visual Inspection**:
   - Examine leaf surfaces for discoloration, spots, lesions, or unusual markings
   - Check for signs of wilting, curling, or structural deformation
   - Look for presence of pest damage (holes, webbing, sticky residue)
   - Assess overall plant vigor and color vibrancy

2. **Symptom Identification**:
   - Identify primary symptoms (what's most visibly wrong)
   - Identify secondary symptoms (supporting indicators)
   - Determine symptom pattern (localized vs. widespread)
   - Note symptom severity (mild, moderate, severe)

3. **Disease Diagnosis**:
   - Match symptoms to known plant diseases
   - Consider environmental stress factors
   - Rule out nutrient deficiencies if applicable
   - Assess probability of each potential diagnosis

4. **Health Assessment**:
   - Rate overall plant health from 0-100
   - Identify factors affecting health (disease, pests, environmental)
   - Assess treatment urgency (routine care vs. emergency intervention)

5. **Recommendations**:
   - Provide specific, actionable treatment steps
   - Include timing and frequency for interventions
   - Suggest environmental adjustments if needed
   - Recommend follow-up monitoring schedule

Please be thorough but concise. Use specific plant disease names and evidence-based treatment methods.
"""

# Template version - can be expanded with plant-specific prompts
DISEASE_SPECIFIC_TEMPLATE = """
Focus analysis on the following diseases:
1. Powdery Mildew - White powdery coating on leaves
2. Leaf Spot - Brown or black circular lesions with rings
3. Rust - Reddish-brown pustules on leaf undersides
4. Blight - Large brown areas affecting stems and leaves
5. Yellowing - Chlorosis from nutrient deficiency or disease
6. Wilting - Drooping despite adequate soil moisture
7. Pest Damage - Holes, webbing, or deformed growth
8. Environmental Stress - Damage from temperature, light, or humidity extremes

For each visible symptom, determine which disease category is most likely.
"""

# Pre-analysis checklist
ANALYSIS_CHECKLIST = """
Before providing your diagnosis, verify:
☐ Plant type is identifiable from the image
☐ Image quality is sufficient for diagnosis (not blurry, has good lighting)
☐ Affected plant parts are clearly visible (leaves, stems, etc.)
☐ Symptoms are visible and not obscured
☐ Multiple angles/areas of plant are considered if visible

If image quality issues exist, note them in your assessment.
"""
