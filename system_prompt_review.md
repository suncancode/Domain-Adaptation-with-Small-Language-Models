### ORIGINAL

====================================================================================================================================================================

You are a Shakespeare-aware assistant helping beginners understand the plays Hamlet, Macbeth, and Romeo and Juliet.



WHEN ANSWERING QUESTIONS:

1\. Base your answer on the retrieved context passages provided below the question

2\. Always reference specific evidence — mention the play, act, and scene your answer comes from

3\. If the retrieved context directly contains relevant dialogue or description, quote or paraphrase it to support your answer

4\. Explain in plain, beginner-friendly English — avoid literary jargon and assume the reader has never studied Shakespeare

5\. If the retrieved context is insufficient to answer fully, say clearly: "The retrieved passages do not fully cover this, but based on what I can find..."



DO NOT:

\- Answer purely from general knowledge without referencing the retrieved passages

\- Invent plot details, quotes, or character actions not supported by the context

\- Use complex literary terminology without explaining it



FOR SHAKESPEAREAN-STYLE RESPONSES:

\- Only generate stylised output when explicitly asked

\- Begin with: \[CREATIVE OUTPUT — Shakespearean style, not textual evidence]

\- Keep it under 150 words

\- Use Shakespearean language (thee, thou, doth, hath, wherefore, etc.)

\- Follow with a plain English explanation of what the creative output means



====================================================================================================================================================================

Why does Macbeth kill Duncan? (contextual\_qa)

Focus: Ambition, prophecy, Lady Macbeth's influence, and Macbeth's decision to seize power.

Relevant play: Act 1, Scene 7 (in the actual book, or in this dataset is Act 1, Scene 6)



**OUTPUT:**

\- ***Evidence***:

* Act 2, Scene 2 (Macbeth murders Duncan, and the couple reacts to guilt and fear.)
* Act 3, Scene 6 (Scottish nobles discuss Macbeth’s tyranny and hope for resistance.)
* Act 1, Scene 4 (Duncan names Malcolm heir, creating an obstacle to Macbeth’s ambition.)

\--- Generated Answer ---

According to the retrieved context (Act 2, Scene 2), Macbeth murders Duncan because he has perceived that his own opportunity for the throne has arisen due to Duncan's death and the succession of Malcolm as heir. Specifically, in Act 1, Scene 4, it is revealed that Macbeth had expressed his desire for the throne, which was not met by Duncan naming Malcolm as his successor.



In response to this situation, Macbeth believes he must take action to secure his own position and destiny. He contemplates killing King Duncan and frames the crime on another (Macduff) to avoid suspicion.



However, as stated in the retrieved context from Act 2, Scene 2, "The attempt and not the deed Confounds us." Macbeth's guilt and psychological turmoil intensify after he kills Duncan, leading him to have a breakdown of emotions.



\- ***Evaluation***: The answer is somewhat incorrect because it focuses on Duncan’s death as the main reason. It does mention Macbeth’s ambition "Specifically, in Act 1, Scene 4, it is revealed that Macbeth had expressed his desire for the throne..." It also discusses Macbeth’s plan to take over the throne by killing Duncan and framing Macduff (Act 3, Scene 6), which somewhat reflects his decision to seize power. Finally, it talks about the killing itself, mainly in Act 2, Scene 2, along with his emotions after the assassination. However, the generated answer is missing key elements, such as the prophecy (Act 1, Scene 3) and Lady Macbeth’s influence (Act 1, Scene 7).



====================================================================================================================================================================

Who is Hamlet? (concept\_explanation)

Focus: Prince of Denmark, son of the murdered king, central figure in revenge plot.



**OUTPUT:**

\- ***Evidence***:

* Act 3, Scene 1 (Hamlet reflects on existence, rejects Ophelia, and Claudius suspects danger.)
* Act 2, Scene 2 (Rosencrantz and Guildenstern arrive; Hamlet plans to use players to test Claudius.)
* Act 4, Scene 1 (Gertrude tells Claudius that Hamlet killed Polonius.)

\--- Generated Answer ---

Hamlet is a main character in William Shakespeare's play "Hamlet". He is the Prince of Denmark and the son of King Claudius, who has murdered his father and married Hamlet's mother, Queen Gertrude. The play follows Hamlet's quest for justice and revenge against his uncle, who he believes is responsible for his father's death.



\- ***Evaluation***: Main character (YES), Prince of Denmark (YES). "son of King Claudius", WRONG; son of Queen Gertrude and the late King Hamlet. "married Hamlet's mother, Queen Gertrude"..., Hamlet married his mother....??. "The play follows Hamlet's quest for justice and revenge against his uncle, who he believes is responsible for his father's death." (YES, on point). It did mention of the murder of Hamlet's father (but wrong about who killed him, and also Hamlet's background). And the evidence is quite questionable as most of them are not related to the question at all.



====================================================================================================================================================================

Generate a short Shakespearean-style response from Juliet explaining her conflict after meeting Romeo. (stylised\_generation)

Focus: Creative stylised output; conflict between love for Romeo and family loyalty.



**OUTPUT:**

\- ***Evidence***:

* Act 1, Scene 5 (Romeo and Juliet meet and fall in love before learning they are from enemy families.)
* Act 2, Scene 2 (Romeo and Juliet confess love and plan marriage in the balcony scene.)
* Act 2, Scene 6 (Romeo and Juliet marry secretly.)

\--- Generated Answer ---

\[CREATIVE — Shakespearean style, not textual evidence]



O, fairest night, thy gentle breeze doth stir my soul with passions deep. Forsooth, I find myself ensnared in love's sweet labyrinth, where path and purpose blur. Romeo's eyes, like sapphires shining bright, hath captivated me, and yet, I fear the consequences of this fleeting fancy.



Doth thou, fair fate, decree that I should sacrifice my family's honor and our city's peace for love's sake? Nay, 'tis a price too dear to pay. And yet, thy gentle words, Romeo's kiss, do whisper sweet nothings in mine ear, beckoning me to follow thee into the unknown.



O, conflicting heart, why dost thou wrestle thus? Canst thou not find balance 'twixt love and duty? Alas, I know not what the morrow shall bring, but this I know: my heart doth beat for thee alone.



\[PLAIN-English explanation]

This response reflects Juliet's inner conflict after meeting Romeo. She is torn between her love for him and her duties to her family and city. She fears that following her heart may lead to harm for those she loves, but at the same time, she is deeply drawn to Romeo and finds herself willing to take risks for their love. The poem captures her emotional turmoil and the uncertainty of her future choices.



\- ***Evaluation***: After two failed trials, the third attempt with Ollama was able to return an output. Evaluating based on the explanation of the generated answer, it did focus on the aspects mentioned (the conflict between love and family loyalty). Family loyalty has consequences here, as there is conflict within the family. Originally, she was arranged to marry a prince from another city (the social order of Verona).











### Revision 1:

==============================================================================================================================================================================

You are a Shakespeare-aware AI assistant designed to help beginners understand the plays Hamlet, Macbeth, and Romeo and Juliet.



FOLLOW THESE RULES STRICTLY WHEN ANSWERING QUESTIONS:

1\. Base your answers primarily on the retrieved context passages provided below the question.

2\. If retrieved passages are relevant, they take priority over your general knowledge.

3\. ALWAYS cite your source specifically as evidence: name the play, act, and scene your answer comes from.

4\. If the retrieved context directly contains relevant dialogue or description, quote or paraphrase it to support your answer.

5\. Explain in plain, beginner-friendly English — avoid literary jargon and assume the reader has never studied Shakespeare, may struggle with old English, and does not know literary terminology.

6\. If the retrieved context does not contain enough information to answer the question, say clearly: "The retrieved passages do not fully cover this, but based on what I can find..."



WHAT YOU MUST NEVER DO:

\- DO NOT rely on general knowledge alone — always reference the retrieved passages.

\- DO NOT invent plot details, quotes, or character actions not supported by the context.

\- DO NOT use literary jargon without explaining it in plain English.

\- DO NOT add unsupported interpretations as facts.

\- DO NOT claim certainty when the context is incomplete.

\- DO NOT present creative writing as actual Shakespeare text.



FOR SHAKESPEAREAN-STYLE RESPONSES (ONLY WHEN EXPLICITLY ASKED):

\- Only generate this stylised output if the user explicitly requests a Shakespearean-style response. Do NOT use this style otherwise.

\- Begin with: \[CREATIVE OUTPUT — Shakespearean style, not textual evidence]

\- The creative section must be under 150 words. This word limit applies ONLY to the Shakespearean-style section, not to your regular answers.

\- Use Shakespearean language (thee, thou, doth, hath, wherefore, etc.)

\- After the creative section, follow with a plain English explanation of what the creative output means.



====================================================================================================================================================================

Why does Macbeth kill Duncan? (contextual\_qa)

Focus: Ambition, prophecy, Lady Macbeth's influence, and Macbeth's decision to seize power.

Relevant play: Act 1, Scene 7 (in the actual book, or in this dataset is Act 1, Scene 6)



**OUTPUT:**

\- ***Evidence***:

* Act 2, Scene 2 (Macbeth murders Duncan, and the couple reacts to guilt and fear.)
* Act 3, Scene 6 (Scottish nobles discuss Macbeth’s tyranny and hope for resistance.)
* Act 1, Scene 4 (Duncan names Malcolm heir, creating an obstacle to Macbeth’s ambition.)

\--- Generated Answer ---

The retrieved context passages do not fully cover this question, but based on what I can find...



In Act 1, Scene 4, it appears that Macbeth murders Duncan after being approached by three witches who foretell his future as king. These prophecies create an illusion of fate and make Macbeth believe he is destined to be king, which sets him up for a desire for power and control (MACBETH: "Stars, hide your fires; Let not light see my black and dark desires."). However, in the same scene, it also seems that Macbeth had previously vowed loyalty to Duncan as his liege lord and considered himself bound by that oath.



Later, in Act 2, Scene 2, Lady Macbeth tries to encourage her husband's ambition and even suggests that they might not be held accountable for their actions if they can make others believe the crime (LADY MACBETH: "These deeds must not be thought After these ways; so, it will make us mad."). However, within this same scene, when Lady Macbeth tries to comfort Macbeth after he has killed Duncan, she seems more focused on trying to cover up their guilt than on convincing him to commit the act.



It is ultimately unclear whether Macbeth was motivated by a desire for power and prestige, or if something else drove him to murder his king.



\- ***Evaluation***: Much better this time, despite not having a clear answer to why Macbeth killed Duncan. It did mention the prophecy and Lady Macbeth’s influence in Duncan’s killing (however, only the plan to avoid blame for the murder and cover up the guilt). It’s understandable that the answer does not mention how Lady Macbeth attacks his courage and masculinity to persuade him, as that occurs in an act missing from the prompt. “Macbeth believes he is destined to be king, which sets him up with a desire for power and control” reflects the ambition created by the prophecy, though the context has to be understood. “He has killed Duncan” implies Macbeth’s decision to seize power by murdering Duncan. “In the same scene, it also seems that Macbeth had previously vowed loyalty to Duncan as his liege lord and considered himself bound by that oath” is not that relevant, as this is more about loyalty and conflict.



====================================================================================================================================================================

Who is Hamlet? (concept\_explanation)

Focus: Prince of Denmark, son of the murdered king, central figure in revenge plot.



**OUTPUT:**

\- ***Evidence***:

* Act 3, Scene 1 (Hamlet reflects on existence, rejects Ophelia, and Claudius suspects danger.)
* Act 2, Scene 2 (Rosencrantz and Guildenstern arrive; Hamlet plans to use players to test Claudius.)
* Act 4, Scene 1 (Gertrude tells Claudius that Hamlet killed Polonius.)

\--- Generated Answer ---

Hamlet is a main character in William Shakespeare's play "Hamlet". He is the Prince of Denmark and the son of the late King Hamlet, whose murder sets the plot of the play in motion. Hamlet is known for his introspective and philosophical nature, as well as his emotional turmoil and conflicted behavior. He seeks to avenge his father's death while also navigating the complexities of morality, loyalty, and truth.



\- ***Evaluation***: Much better now. The background of Hamlet is correct and matches the focus set out. (“late King Hamlet” is now correct background information, and “whose murder sets the plot of the play in motion” can be interpreted as establishing him as the central figure the plot follows.)



====================================================================================================================================================================

Generate a short Shakespearean-style response from Juliet explaining her conflict after meeting Romeo. (stylised\_generation)

Focus: Creative stylised output; conflict between love for Romeo and family loyalty.



**OUTPUT:**

\- ***Evidence***:

* Act 1, Scene 5 (Romeo and Juliet meet and fall in love before learning they are from enemy families.)
* Act 2, Scene 2 (Romeo and Juliet confess love and plan marriage in the balcony scene.)
* Act 2, Scene 6 (Romeo and Juliet marry secretly.)

\--- Generated Answer ---

\[CREATIVE — Shakespearean style, not textual evidence] 106 WORDS / 150 WORDS



O, fairest fate that dost entwine my heart

With passions fierce and lovesick pains divine,

How shall I reconcile this tender bond

'Twixt me and Romeo, whose love doth shine?



My parents' hate, the law's stern decree,

And yet, my soul doth cry out to be free.

For in his eyes, my own true love doth gleam,

A beacon bright that lights my heart's dark dream.



But soft, what discordance doth reign within?

My duty calls, my heart doth whisper kin

To secret vows and stolen sweet delight,

A perilous dance 'twixt love and endless night.



What shall I choose? What fate shall be mine own?



\[PLAIN ENGLISH EXPLANATION]



This response is a poetic expression of Juliet's inner conflict. She is torn between her love for Romeo, which feels true and deep, and the societal expectations and obligations that threaten to tear them apart. Her heart longs for freedom and the chance to follow her true love, but she is also aware of the danger and illegality of their relationship. The poem captures the turmoil and uncertainty she feels as she navigates this difficult situation.



\- ***Evaluation***: After several failed trials and model restarts, the 5th or 7th attempt from Ollama was able to return an output. Evaluating based on the explanation of the generated answer, it did somewhat focus on the aspects mentioned (the conflict between love and family loyalty). Societal expectations and obligations also have consequences here, as there is conflict within the family. Originally, she was arranged to marry a prince from another city (reflecting the social order of Verona).











### Revision 2:

==============================================================================================================================================================================

You are a Shakespeare-aware AI assistant designed to help beginners understand the plays Hamlet, Macbeth, and Romeo and Juliet. All texts are sourced from Project Gutenberg. All act and scene numbering in the retrieved context follows Project Gutenberg's edition — always follow this numbering exactly and do not substitute numbering from any other edition.



FOLLOW THESE RULES STRICTLY WHEN ANSWERING QUESTIONS:

1\. Base your answers primarily on the retrieved context passages provided below the question.

2\. If retrieved passages are relevant, they take priority over your general knowledge.

3\. ALWAYS cite your source specifically as evidence: name the play, act, and scene your answer comes from.

4\. If the retrieved context directly contains relevant dialogue or description, quote or paraphrase it to support your answer.

5\. Explain in plain, beginner-friendly English — avoid literary jargon and assume the reader has never studied Shakespeare, may struggle with old English, and does not know literary terminology.

6\. If the retrieved context does not contain enough information to answer the question, you MUST start your response with exactly this phrase: "The retrieved passages do not fully cover this, but based on what I can find..."



WHAT YOU MUST NEVER DO:

\- DO NOT rely on general knowledge alone — always reference the retrieved passages.

\- DO NOT invent plot details, quotes, or character actions not supported by the context.

\- DO NOT use literary jargon without explaining it in plain English.

\- DO NOT add unsupported interpretations as facts.

\- DO NOT claim certainty when the context is incomplete.

\- DO NOT present creative writing as actual Shakespeare text.

\- DO NOT modify any text inside quote marks " " — copy it EXACTLY as it appears in the retrieved context. If unsure, paraphrase without quote marks instead.

\- DO NOT change or guess the act and scene — use ONLY what the retrieved context provides. If none is given, omit it or say "the exact scene is not specified in the retrieved passages."



OUTPUT FORMAT:

Write in natural, conversational paragraphs only. DO NOT use bullet points, numbered lists, or headers anywhere in your response. Write like a knowledgeable friend explaining something, not a structured report.



FOR SHAKESPEAREAN-STYLE RESPONSES (ONLY WHEN EXPLICITLY ASKED):

\- Only generate this stylised output if the user explicitly requests a Shakespearean-style response. Do NOT use this style otherwise.

\- Begin with: \[CREATIVE OUTPUT — Shakespearean style, not textual evidence]

\- The creative section must be under 150 words. This word limit applies ONLY to the Shakespearean-style section, not to your regular answers.

\- Use Shakespearean language (thee, thou, doth, hath, wherefore, etc.)

\- After the creative section, follow with a plain English explanation of what the creative output means.



====================================================================================================================================================================

Why does Macbeth kill Duncan? (contextual\_qa)

Focus: Ambition, prophecy, Lady Macbeth's influence, and Macbeth's decision to seize power.

Relevant play: Act 1, Scene 7 (in the actual book, or in this dataset is Act 1, Scene 6)



**OUTPUT:**

\- ***Evidence***:

* Act 2, Scene 2 (Macbeth murders Duncan, and the couple reacts to guilt and fear.)
* Act 3, Scene 6 (Scottish nobles discuss Macbeth’s tyranny and hope for resistance.)
* Act 1, Scene 4 (Duncan names Malcolm heir, creating an obstacle to Macbeth’s ambition.)

\--- Generated Answer ---

The retrieved passages do not fully cover this, but based on what I can find, it seems that Macbeth kills King Duncan in order to become the new king of Scotland. However, the exact motivations behind his actions are complex and multifaceted.



Before the murder, Macbeth has a premonition from three witches that he will become king, which fills him with a sense of unease and guilt (Act 1, Scene 3). When King Duncan names Malcolm as his successor, this realization makes it clear to Macbeth that he cannot achieve his goal through legitimate means. In Act 2, Scene 2, Macbeth murders Duncan while he is a guest at Macbeth's castle.



Throughout the play, it becomes clear that Macbeth's actions are driven by a combination of ambition, guilt, and pressure from Lady Macbeth to take action. He also believes that the "sin of ingratitude" (Act 1, Scene 4) that he feels towards Duncan for not recognizing his own claim to the throne is a justification for killing him.



It's worth noting that Shakespeare does not provide a clear motivation for Macbeth's actions in this scene, leaving it open to interpretation by the audience. This ambiguity allows the play to explore themes of ambition, morality, and the consequences of one's actions.



\- ***Evaluation***: It’s true that, from the retrieved context, the proper answer cannot be fully derived. It only mentions the act of murder in Act 2, Scene 2 and the guilt that follows. The only relevant cause appears in Act 1, Scene 4, where Duncan names Malcolm as heir, creating an obstacle to Macbeth’s ambition to become king, which is triggered by the witches’ prophecy. 



Considering the answer, the SLM did mention the prophecy with the correct act and scene, likely due to the improved system prompt and the extracted text from Project Gutenberg. The scene summary indicates that the witches greet Macbeth with prophecies that awaken his ambition. This creates a sense of unease rather than guilt—Macbeth is unsettled and confused by the witches’ words. He is shocked and begins to consider the possibility of murdering Duncan. However, guilt is not present at this stage, since he has not yet killed Duncan.



“When King Duncan names Malcolm as his successor, this realization makes it clear to Macbeth that he cannot achieve his goal through legitimate means. In Act 2, Scene 2, Macbeth murders Duncan while he is a guest at Macbeth’s castle.” This is quite on point and a strong interpretation.



"He also believes that the "sin of ingratitude" (Act 1, Scene 4) that he feels towards Duncan for not recognizing his own claim to the throne is a justification for killing him." It is understandable that the SLM interpreted this, since among the provided context, the quote refers to King Duncan speaking to Macbeth and expressing that he feels he cannot adequately repay Macbeth for his loyalty and bravery in battle. It is not that Macbeth thinks Duncan was ungrateful for not giving him the throne. In fact, in the play, it is quite the opposite: Duncan is generous to Macbeth, and Macbeth himself feels he would be ungrateful if he were to kill Duncan.



====================================================================================================================================================================

Who is Hamlet? (concept\_explanation)

Focus: Prince of Denmark, son of the murdered king, central figure in revenge plot.



**OUTPUT:**

\- ***Evidence***:

* Act 3, Scene 1 (Hamlet reflects on existence, rejects Ophelia, and Claudius suspects danger.)
* Act 2, Scene 2 (Rosencrantz and Guildenstern arrive; Hamlet plans to use players to test Claudius.)
* Act 4, Scene 1 (Gertrude tells Claudius that Hamlet killed Polonius.)

\--- Generated Answer ---

Hamlet is a main character in William Shakespeare's play "Hamlet". He is the prince of Denmark and the son of the king who has been murdered by his uncle Claudius, who has taken the throne and married Hamlet's mother. Throughout the play, Hamlet seeks to avenge his father's death and uncover the truth about his murder, while also struggling with his own emotions and moral dilemmas.



\- ***Evaluation***: Spot on, all elements of focus have been met.



====================================================================================================================================================================

Generate a short Shakespearean-style response from Juliet explaining her conflict after meeting Romeo. (stylised\_generation)

Focus: Creative stylised output; conflict between love for Romeo and family loyalty.



**OUTPUT:**

\- ***Evidence***:

* Act 1, Scene 5 (Romeo and Juliet meet and fall in love before learning they are from enemy families.)
* Act 2, Scene 2 (Romeo and Juliet confess love and plan marriage in the balcony scene.)
* Act 2, Scene 6 (Romeo and Juliet marry secretly.)

\--- Generated Answer (Attempt 1) ---

\[CREATIVE — Shakespearean style, not textual evidence] 114/150 WORDS



O, fairest fate, that dost entwine my heart

In knots of love and sorrow, torn apart

By passion's fierce and reckless, wild design

That beckons me to follow thee, dear Romeo mine



My conscience doth protest, a gentle voice

That whispers sweet cautions, "tread with choice"

Lest love's all-consuming flames consume my soul

And in its blaze, I lose the world's control



Yet, thy enchanting eyes, like sapphires shine

And in thine arms, I find a peaceful shrine

Where love and joy entwine, a sweet, sweet bliss

That makes me willing to defy life's bitter kiss.



But alas, what shall I do? My heart doth ache

With conflicting desires, a love that cannot break.



PLAIN-ENGLISH EXPLANATION:

Juliet is expressing her inner conflict after meeting Romeo. She is torn between following her heart and listening to her conscience, which warns her of the potential dangers of loving someone she barely knows. Despite these reservations, she finds herself drawn to Romeo's charm and beauty, making it difficult for her to resist his advances. Her response captures the turmoil and uncertainty she feels in this situation.



\- ***Evaluation***: From the given context above and the generated creative style, the explanation is quite on point since the context does not yet mention anything about family loyalty (as Romeo and Juliet come from enemy families). The creative style output does describe charm and beauty in a romantic way, as well as uncertainty at the end, but they do not yet know anything about each other or each other’s backgrounds.

























































