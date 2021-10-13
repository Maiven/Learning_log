import pandas as pd
import numpy as np

#제출자 리스트(수기 입력)
videos = ['조용원', '정태호', '정우민', '장진희', '임채은', '이승수', '이남준', '윤다솜', '오유리나', '신수아', '백송하', '박원빈', '김현우', '김현수', '김태호', '김태연', '김의식', '김영우', '김세형', '강지호', '강수현']
#Urclass 수강생 현황 csv 불러오기
df = pd.read_csv('1012.csv')

def group_maker(random_seed, video=len(videos), videos=videos, ur_list=df, group_num=7):
    """
    인원 배치는 랜덤이되 각 조에 제출자의 수가 일정하게 들어가게끔 프로젝트 조 짜는 함수입니다

    --파라미터--
    * Random seed
    * video = 실제 제출자 수 (int) -> 제출자 명단이 잘 입력됐나 확인하기 위함
    * videos = 제출자 명단 (list)
    * ur_list = Urclass에서 export한 기수 명단 (dataframe)
    * group_num = 조 수 (int)
    """
    try:
        assert len(videos) == video #제출자 명단이 잘 입력되었는지 확인

        #미제출자 리스트
        non_videos = [name for name in ur_list['이름'].values if name not in videos]

        try: #미제출자 리스트가 잘 뽑혔는지 확인 (한글이라 잘못 뽑히는 경우 있음)
            assert len(videos) + len(non_videos) == len(ur_list)

            #조 배정 시작!
            np.random.seed(random_seed)
            np.random.shuffle(videos)
            np.random.shuffle(non_videos)

            video = int(len(videos)/group_num) #한 조 최소 제출자 인원
            non_video = int(len(non_videos)/group_num) #한 조 최소 미제출자 인원
            groups = {}

            for i in range(group_num+1):
                if i == group_num:
                    #1조부터 미제출자 나머지 인원 배치
                    for j in range(len(non_videos[non_video*i:])):
                        groups[f'{j+1}조'].append(non_videos.pop())
                    
                    #뒷 조부터 제출자 나머지 인원 배치
                    for j in range(len(videos[video*i:])):
                        groups[f'{group_num-j}조'].append(videos.pop())

                    return groups
                
                group = videos[video*i:video*(i+1)]
                group = group + non_videos[non_video*i:non_video*(i+1)]
                groups[f'{i+1}조'] = group
        
        except:
            print(f'미 제출자 리스트를 확인하세요')
            print(f'\t* 총 인원 수: {len(ur_list)}명, \n\t* 미 제출자 리스트: {len(non_videos)}명, \n{non_videos}, \n\t* 제출자 리스트: {len(videos)}명, {videos}')
    
    except:
        print('입력한 제출자 인원 수와 제출자 명단에 있는 수가 일치하지 않습니다. 제출자 명단을 확인해 주세요')

if __name__ == "__main__":
    #그룹 만들기
    groups = group_maker(random_seed=1012, video=21)

    #명단 출력
    for group in groups:
        print(groups.get(group))
    
    #수강생 이름이 빠짐없이 들어갔는지 재확인
    j=0
    for group in groups:
        i = len(groups.get(group))
        j += i

    assert j == len(df)
