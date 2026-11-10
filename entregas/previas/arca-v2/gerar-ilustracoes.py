"""Original command-generated SVG studies: projected wooden hull, cutaway and plan.
Reference is a user-supplied concept image, not an archaeological or engineering source.
"""
from pathlib import Path
import math,random,html
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'gerados';OUT.mkdir(parents=True,exist_ok=True)
random.seed(61016)
INK='#3e382c';PAPER='#ece4d1';ORANGE='#cc6035';TEAL='#325d54'
def fmt(x):return f'{x:.2f}'
def rgb(c):return '#'+''.join(f'{max(0,min(255,round(x))):02x}' for x in c)
def esc(x):return html.escape(str(x))
def text(x,y,s,size=24,color=INK,anchor='start',bold=False,serif=False):
 return f'<text x="{x}" y="{y}" font-family="{("DejaVu Serif" if serif else "DejaVu Sans")}" font-size="{size}" fill="{color}" text-anchor="{anchor}"'+(' font-weight="bold"' if bold else '')+f'>{esc(s)}</text>'
def line(x1,y1,x2,y2,color=INK,w=1.5,dash=''):
 return f'<path d="M{x1},{y1}L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>'
def label(x,y,head,body):
 return text(x,y,head,19,TEAL,bold=True)+text(x,y+31,body,18)
def shell(title,subtitle,body,number):
 grid=''.join(line(x,220,x,1010,'#b7aa8a',.55) for x in range(60,1941,40))+''.join(line(60,y,1940,y,'#b7aa8a',.55) for y in range(250,1011,40))
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="1200" viewBox="0 0 2000 1200"><defs><filter id="paper"><feTurbulence type="fractalNoise" baseFrequency=".62" numOctaves="3" seed="14"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="linear" slope=".055"/></feComponentTransfer></filter><pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M-2 8L8-2M3 13L13 3" stroke="#6a5637" stroke-width=".6" opacity=".4"/></pattern><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{INK}"/></marker></defs><rect width="2000" height="1200" fill="{PAPER}"/><g opacity=".2">{grid}</g><rect width="2000" height="1200" filter="url(#paper)" opacity=".65"/>{text(74,65,'PAPIRO REVELA',25,TEAL,bold=True)}{text(1925,65,f'ESTUDO {number} · PARA APROVAÇÃO',18,anchor='end')}{line(74,90,1926,90,'#a79a7b',1)}{text(74,160,title,49,bold=True)}{text(76,202,subtitle,23,serif=True)}{body}{line(74,1072,1926,1072,'#a79a7b',1)}{text(74,1112,'FONTE: GÊNESIS 6:14–16',20,TEAL,bold=True)}{text(74,1151,'Interpretação artística. Forma do casco, cobertura e detalhes de construção não são especificados integralmente no texto.',18)}{text(1925,1112,'MEDIDAS EM CÔVADOS · SEM CONVERSÃO FIXA EM METROS',17,anchor='end')}{text(1925,1151,'Ilustração original em SVG, criada por código. Sem geração de voz ou vídeo.',16,anchor='end')}</svg>'''
# Parametric, symmetrical long hull. x:length, y:beam, z:height.
L=300.;B=50.;H=30.;A=math.radians(24);E=math.radians(27);S=4.8
OX,OY=1010,690
objects=[]
def proj(p):
 x,y,z=p
 return (OX+S*(x*math.cos(A)-y*math.sin(A)),OY+S*(x*math.sin(A)*math.sin(E)+y*math.cos(A)*math.sin(E)-z*math.cos(E)))
def depth(p):
 x,y,z=p;return x*math.sin(A)*math.cos(E)+y*math.cos(A)*math.cos(E)+z*math.sin(E)
def point(x,t,side):
 # Flared U sections; smoothly rounded ends, no bowl-like compressed length.
 u=min(1,abs(x)/(L/2));width=B/2*max(0,1-u**12)**.43
 base=13*u**14
 return (x,side*width*math.sqrt(max(0,2*t-t*t)),base+(H-base)*t)
def poly(pts,fill,stroke='none',w=.8):
 d=sum(depth(p) for p in pts)/len(pts)
 xy=' '.join(f'{fmt(x)},{fmt(y)}' for x,y in map(proj,pts))
 objects.append((d,f'<polygon points="{xy}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>'))
def path3(pts,color,w=1,opacity=1):
 d=sum(depth(p) for p in pts)/len(pts)+.015
 xy=' '.join(f'{fmt(x)},{fmt(y)}' for x,y in map(proj,pts))
 objects.append((d,f'<polyline points="{xy}" fill="none" stroke="{color}" stroke-width="{w}" opacity="{opacity}" stroke-linecap="round" stroke-linejoin="round"/>'))
NX=100;NT=20
for side in [-1,1]:
 for j in range(NT):
  for k in range(NX):
   x=-150+300*k/NX;xx=-150+300*(k+1)/NX;t=j/NT;tt=(j+1)/NT
   pts=[point(x,t,side),point(xx,t,side),point(xx,tt,side),point(x,tt,side)]
   light=.80+.18*(1-t)+.055*math.sin((k+.5)*.13)+(.07 if side<0 else 0)
   grain=(j%3-1)*3
   poly(pts,rgb([168*light+grain,127*light+grain,77*light+grain]))
  for k in range(NX):path3([point(-150+300*k/NX,j/NT,side),point(-150+300*(k+1)/NX,j/NT,side)],'#604a2f',.75,.68)
  for k in range(8):
   xx=-134+k*38+(j%2)*16
   if xx<145:path3([point(xx,(j+.05)/NT,side),point(xx,(j+.93)/NT,side)],'#53432e',.7,.65)
  # Fine hand-etched grain, kept short and staggered along each board.
  for q in range(33):
   xx=random.uniform(-143,131);length=random.uniform(3,12);t0=(j+random.uniform(.18,.8))/NT
   pts=[point(min(149,xx+length*r/5),t0+math.sin(r*1.1+q)*.0011,side) for r in range(6)]
   path3(pts,'#55452f',.45,random.uniform(.25,.5))
# Broad gunwale outline and a planked top deck.
xs=[-150+300*k/NX for k in range(NX+1)]
outline=[point(x,1,1) for x in xs]+[point(x,1,-1) for x in reversed(xs)]
poly(outline,'#b69b6b','#4a3d2b',1.6)
# Deck planks in segments; surface is narrow compared with the long hull.
for yy in range(-20,22,3):
 pts=[]
 for x in xs:
  limit=abs(point(x,1,1)[1])
  if abs(yy)<limit:pts.append((x,yy,30.15))
 if pts:path3(pts,'#75603e',.8,.8)
for side in [-1,1]:
 path3([point(x,1,side) for x in xs],'#443b2b',4,.95)
 path3([(p[0],p[1],p[2]+.9) for p in [point(x,1,side) for x in xs]],'#dac79e',1.3,.9)
# Long, low shelter. It follows the hull; not a tall triangular hat.
a,b=-111,111;wy=16;z=30.4;wall=37;ridge=42
poly([(a,-wy,z),(b,-wy,z),(b,-wy,wall),(a,-wy,wall)],'#a88b59','#57452e',1.2)
poly([(a,wy,z),(b,wy,z),(b,wy,wall),(a,wy,wall)],'#947646','#57452e',1.5)
for x in [a,b]:poly([(x,-wy,z),(x,wy,z),(x,wy,wall),(x,0,ridge),(x,-wy,wall)],'#b79a65','#57452e',1.5)
poly([(a-4,-wy-2,wall),(b+4,-wy-2,wall),(b+4,0,ridge),(a-4,0,ridge)],'#977b4e','#4e422e',1.4)
poly([(a-4,wy+2,wall),(b+4,wy+2,wall),(b+4,0,ridge),(a-4,0,ridge)],'#816c47','#4e422e',1.4)
for x in range(-113,115,4):
 path3([(x,-18,37.3),(x,0,42.2),(x,18,37.3)],'#4e422f',.65,.65)
for y in [-14,-10,-6,6,10,14]:
 zz=42-abs(y)/18*5+.15;path3([(-114,y,zz),(114,y,zz)],'#c3ac7b',.55,.6)
# Small schematic upper openings; decorative form is not claimed as a biblical specification.
for x in range(-100,111,22):poly([(x,16.12,31.8),(x+6,16.12,31.8),(x+6,16.12,35.2),(x,16.12,35.2)],'#39392d','#493b2a',.5)
# Side doorway on the visible flank. Attach to the hull surface, not a house wall.
doorx=38
for k in range(12):
 x=doorx+k/12*12;xx=doorx+(k+1)/12*12
 poly([point(x,.19,1),point(xx,.19,1),point(xx,.78,1),point(x,.78,1)],'#38362b')
for xx in [doorx,doorx+12]:path3([point(xx,t,1) for t in [.19,.3,.4,.5,.6,.7,.78]],'#d3ba83',2,.9)
for t in [.19,.78]:path3([point(doorx,t,1),point(doorx+12,t,1)],'#c9af7e',2,.9)
# Ribs reinforce the rounded fore/stern contour.
for x in [-145,-139,139,145]:path3([point(x,j/50,1) for j in range(51)],'#493b29',2.2,.9)
# Light grounding shadow, outside the ship's geometry.
body='<ellipse cx="1030" cy="842" rx="620" ry="34" fill="#6b5b3b" opacity=".08"/>'
body+=''.join(v for _,v in sorted(objects,key=lambda q:q[0]))
# Roof detail is overlaid on its visible surfaces after the hull painter pass.
def overlay3(pts,color,w=1,opacity=1):
    xy=' '.join(f'{fmt(x)},{fmt(y)}' for x,y in map(proj,pts))
    return f'<polyline points="{xy}" fill="none" stroke="{color}" stroke-width="{w}" opacity="{opacity}"/>'
for x in range(-113,115,4):
    body+=overlay3([(x,-18,37.3),(x,0,42.2),(x,18,37.3)],'#4e422f',.7,.65)
for y in [-14,-10,-6,6,10,14]:
    zz=42-abs(y)/18*5+.15
    body+=overlay3([(-114,y,zz),(114,y,zz)],'#d0bb8b',.65,.65)
for x in range(-100,111,22):
    xy=' '.join(f'{fmt(a)},{fmt(b)}' for a,b in map(proj,[(x,16.15,31.8),(x+6,16.15,31.8),(x+6,16.15,35.2),(x,16.15,35.2)]))
    body+=f'<polygon points="{xy}" fill="#39392d"/>'
for x in [-150,150]:
    body+=overlay3([(x,0,14),(x,0,34)],'#5a472e',6,.95)
    body+=overlay3([(x,0,15),(x,0,34)],'#c6aa77',1.6,.95)

# Leader annotations live outside the hull.
qx,qy=proj((44,point(44,.5,1)[1],15))
body+=line(qx,qy,1530,892,TEAL,1.7)+line(1530,892,1840,892,TEAL,1.7)
body+=label(1540,928,'PORTA NA LATERAL','Detalhe mencionado em Gn 6:16.')
rx,ry=proj((30,0,42))
body+=line(rx,ry,1320,315,TEAL,1.7)+line(1320,315,1820,315,TEAL,1.7)
body+=label(1340,259,'COBERTURA BAIXA','Forma artística, não uma planta bíblica.')
body+=label(88,918,'CASCO ALONGADO E EXTREMIDADES ARREDONDADAS','Linguagem visual orientada pela referência fornecida.')
body+=text(90,1010,'01 / PERSPECTIVA EXTERNA',23,ORANGE,bold=True)
(OUT/'01-arca-perspectiva.svg').write_text(shell('A ARCA COMO EMBARCAÇÃO','Casco comprido, madeira aparente e cobertura acompanhando o comprimento.',body,'01'))
# Longitudinal section: keep length/height proportional (300:30), annotate the three interior levels.
x0,y0,sc=260,665,4.9
X=lambda x:x0+x*sc
Y=lambda z:y0-z*sc
hull=f'M{X(0)} {Y(30)} Q{X(0)} {Y(0)} {X(27)} {Y(0)} H{X(273)} Q{X(300)} {Y(0)} {X(300)} {Y(30)} Z'
body=f'<path d="{hull}" fill="#bea273" stroke="{INK}" stroke-width="5"/>'
body+=f'<clipPath id="section"><path d="{hull}"/></clipPath><g clip-path="url(#section)">'
for n in range(3):
 body+=f'<rect x="{X(2)}" y="{Y((n+1)*10)}" width="{296*sc}" height="{10*sc}" fill="{["#c3aa80","#ddccaa","#eadcc1"][n]}"/>'
for zz in [10,20]:body+=line(X(2),Y(zz),X(298),Y(zz),'#6a5030',5)
for xx in range(24,290,22):
 body+=line(X(xx),Y(0),X(xx),Y(30),'#81623b',3)
for xx in range(0,301,9):
 body+=line(X(xx),Y(0),X(xx),Y(3),'#765632',2)
body+='</g>'+f'<path d="{hull}" fill="none" stroke="{INK}" stroke-width="5"/>'
# Shelter in side elevation, much lower than the hull.
body+=f'<path d="M{X(33)} {Y(30)} V{Y(37)} H{X(267)} V{Y(30)}" fill="#b99c67" stroke="{INK}" stroke-width="3"/>'
body+=line(X(29),Y(37),X(271),Y(37),INK,5)
for xx in range(41,261,17):body+=f'<rect x="{X(xx)}" y="{Y(35.5)}" width="{6*sc}" height="{3*sc}" fill="#4f4835"/>'
for j,(name,zz) in enumerate([('TERCEIRO',25),('SEGUNDO',15),('INFERIOR',5)]):
 yy=Y(zz)
 body+=f'<rect x="{X(120)}" y="{yy-17}" width="290" height="34" rx="3" fill="{PAPER}" opacity=".95"/>'
 body+=text(X(120)+145,yy+8,f'{3-j} · {name}',21,TEAL,anchor='middle',bold=True)
body+=text(1000,357,'CORTE LONGITUDINAL — TRÊS NÍVEIS',28,TEAL,anchor='middle',bold=True)
body+=label(260,760,'COMPARTIMENTOS','Divisões mostradas apenas para explicar o texto, sem definir uma distribuição exata.')
body+=label(260,844,'COBERTURA E ESTRUTURA','O desenho não acrescenta medidas obrigatórias para as partes que o relato não detalha.')
body+=text(260,1010,'02 / INTERIOR ESQUEMÁTICO',23,ORANGE,bold=True)
body+=line(X(0),Y(-13),X(300),Y(-13),INK,1.4)
body+=text(1000,Y(-13)-10,'300 CÔVADOS DE COMPRIMENTO',20,anchor='middle')
(OUT/'02-arca-corte.svg').write_text(shell('OS TRÊS NÍVEIS DA ARCA','Inferior, segundo e terceiro — uma visualização de Gênesis 6:16.',body,'02'))
# Top view with dimensions stated in the text, not a meter conversion.
x0,y0,sc=260,558,4.9
X=lambda x:x0+x*sc
Y=lambda y:y0+y*sc
body=f'<rect x="{X(0)}" y="{Y(-25)}" width="{300*sc}" height="{50*sc}" rx="{25*sc}" fill="#b69b6f" stroke="{INK}" stroke-width="4"/>'
for yy in range(-21,23,3):
 inset=25-math.sqrt(max(0,25**2-yy**2));body+=line(X(inset),Y(yy),X(300-inset),Y(yy),'#7a6441',1)
body+=f'<rect x="{X(38)}" y="{Y(-16)}" width="{224*sc}" height="{32*sc}" fill="#8f794e" stroke="{INK}" stroke-width="3"/>'
for xx in range(39,263,4):body+=line(X(xx),Y(-16),X(xx),Y(16),'#bbaa80',.9)
body+=line(X(38),Y(0),X(262),Y(0),'#4b422f',4)
body+=f'<path d="M{X(0)} {Y(-39)} H{X(300)}" stroke="{INK}" stroke-width="1.6" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
body+=line(X(0),Y(-28),X(0),Y(-44),INK,1)+line(X(300),Y(-28),X(300),Y(-44),INK,1)
body+=text(1000,Y(-39)-16,'300 CÔVADOS · COMPRIMENTO',23,anchor='middle',bold=True)
body+=f'<path d="M{X(318)} {Y(-25)} V{Y(25)}" stroke="{INK}" stroke-width="1.6" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
body+=text(X(318)+20,y0-8,'50',29,bold=True)+text(X(318)+20,y0+24,'CÔVADOS',14)+text(X(318)+20,y0+48,'DE LARGURA',14)
body+=text(1000,778,'ALTURA DO CASCO: 30 CÔVADOS',24,anchor='middle',bold=True)
body+=label(260,866,'300 × 50 × 30','Comprimento, largura e altura, conforme Gênesis 6:15.')
body+=text(260,942,'O côvado é uma unidade antiga; não fixamos uma equivalência em metros.',22,serif=True)
body+=text(260,1010,'03 / VISTA SUPERIOR E MEDIDAS',23,ORANGE,bold=True)
(OUT/'03-arca-medidas.svg').write_text(shell('AS MEDIDAS DO RELATO','Proporção de referência: 300 de comprimento, 50 de largura e 30 de altura.',body,'03'))
print('Três estudos SVG gerados em',OUT)
