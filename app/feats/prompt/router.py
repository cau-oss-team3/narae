"""
라우터의 역할: Model View Controller -> URL 매핑하는 역할
어떤 파라미터를 받고 어떻게 요청하는지에 대한 코드
서비스를 호출하고 GPT 리소스를 제공하는 코드
"""

"""
Action: 오늘 당장 실행할 수 있는 Task
커리큘럼: 사용자의 장기적인 학습 행동 방침 - 장기간의 거대한 목표, 체계적인 지식 습득 위함, 향후 참조할 대량의 자료, 마일스톤
학습방향: 사용자의 단기적인 학습 행동 방침 - 단기간의 일시적 목표, 자신의 능력 향상을 위함, 지금 참조할 소량의 자료, 플래그

시스템 프롬프트의 의도 [평가표] <- 만점이 나오도록 프롬프트 엔지니어링을 해야 함 (별도의 프롬프트로 분리)
기본 전제: (포기하지 않도록 동기 부여를 해줘야 한다.)

1. 다음에 해야 하는 ***학습 방향***을 제시해줘야 한다.
   - DB에 저장해서 사용자가 다시 찾아볼 수 있도록 제공한다.
   - 오늘 접속한 경우 띄워준다.
   - 액션을 하기 전 사용자가 학습 방향을 먼저 제시받아야 한다.
2. 오늘 학습 방향에 따라 실천 가능한 ***액션을*** 추천한다.
   - 이때 실천 가능할만큼 구체적이고 적절한 난이도의 조언을 해야 한다.
   - 내가 처음인지/어디까지 해봤는지 알아야 한다.
   - 액션을 어떻게 완수했는지 알릴 수 있어야 한다. 액션 완수 내용을 말하면 피드백 해줘야 한다.
   - 액션 포기가 가능해야 한다. 포기하는 경우 이유를 말해고 다음 액션을 추천해준다.(+서버에 저장)
3. 나의 관심분야에 대한 질문에 ***답***을 해줘야 한다.
   - 기본적인 채팅의 형태로 이루어진다.
   - 임베딩이 사용할 수 있으면 좋다.
"""
from fastapi import APIRouter, Depends
from openai import OpenAI

from .schemas import GPTRequest, GPTResponse
from .depends import get_openai_client
from .service import MyService

router = APIRouter(prefix="/prompt", tags=["prompt"])

service = MyService()


@router.post(
    "/gpt-test/",
    description="Simple demo for testing GPT-3.5-turbo model",
    response_model=GPTResponse,
)
async def gpt_test(request: GPTRequest, client: OpenAI = Depends(get_openai_client)):
    response = service.get_coaching_info_from_gpt(client, request.sticc)
    return GPTResponse(response)
