exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { messages } = JSON.parse(event.body);

    const API_URL = 'https://api.groq.com/openai/v1/chat/completions';
    const HEADERS = {
      'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
      'Content-Type': 'application/json'
    };

    const getPayload = (modelName) => JSON.stringify({
      model: modelName,
      messages: messages,
      temperature: 0.7,
      max_tokens: 400,
      stream: false
    });

    let response;
    let primaryModel = 'meta-llama/llama-4-scout-17b-16e-instruct';
    let fallbackModel = 'llama-3.1-8b-instant';

    console.log(`Attempting request with model: ${primaryModel}`);

    try {
      // Attempt 1: Primary Model
      response = await fetch(API_URL, {
        method: 'POST',
        headers: HEADERS,
        body: getPayload(primaryModel)
      });

      // If primary fails (limit reached, error, not found), throw to trigger fallback
      if (!response.ok) {
        console.warn(`Primary model failed (Status: ${response.status}). Initiating fallback...`);
        throw new Error('Trigger fallback');
      }
    } catch (e) {
      // Attempt 2: Fallback Model
      console.log(`Executing fallback with model: ${fallbackModel}`);
      response = await fetch(API_URL, {
        method: 'POST',
        headers: HEADERS,
        body: getPayload(fallbackModel)
      });
      
      if (!response.ok) {
        throw new Error(`Both models failed. Final status: ${response.status}`);
      }
    }

    const data = await response.json();

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify(data)
    };
  } catch (error) {
    console.error('Chat Error Handled:', error.message);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'All chosen AI models failed to respond.', details: error.message })
    };
  }
};
